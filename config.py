from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from flask import current_app, url_for, render_template
from itsdangerous import URLSafeTimedSerializer

mysql = MySQL()
mail = Mail()

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration  # Token expires after 1 hour
        )
    except:
        return False
    return email

def send_email(email_to:str, subject:str, body_text:str, route:str):
    """
    sends a mail to email_to
    :param email_to: to whose email to send
    :param subject: subject of the email
    :param body_text: should contain a plain text message with '{url}' in the place of the url
    :param route: a route, to which url points, it should have a 'token' argument
    :return:
    """
    token = generate_token(email_to)
    url = url_for(route, token=token, _external=True)
    subject = subject.encode('utf-8')
    body = body_text.format(url=url).encode('utf-8')
    msg = Message(subject.decode('utf-8'), recipients=[email_to], body=body.decode('utf-8'))
    msg.charset = 'utf-8'
    mail.send(msg)

def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    verification_url = url_for('home.verify_email', token=token, _external=True)
    subject = "Please verify your email".encode('utf-8')
    body = f"Click the link to verify your email: {verification_url}".encode('utf-8')

    # Send the email
    msg = Message(subject=subject.decode('utf-8'), recipients=[user_email], body=body.decode('utf-8'))
    msg.charset = 'utf-8'  # Set the encoding explicitly
    mail.send(msg)

def send_change_password_email(user_email):
    token = generate_verification_token(user_email)
    url = url_for('profile.change_password', token=token, _external=True)
    subject = "Password change".encode('utf-8')
    body = f"Click the link to change your password: {url}".encode('utf-8')

    msg = Message(subject=subject.decode('utf-8'), recipients=[user_email], body=body.decode('utf-8'))
    msg.charset = 'utf-8'
    mail.send(msg)