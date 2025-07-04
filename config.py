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
    send_email(
        email_to=user_email,
        subject="Please verify your email",
        body_text="Click the link to verify your email: {url}",
        route='home.verify_email'
    )

def send_email_with_url(email_to:str, url:str, subject:str, body_text:str):
    subject = subject.encode('utf-8')
    body = body_text.format(url=url).encode('utf-8') # ten url tutaj musi być już z tokenem, ale zbudować url-a można tylko w user.py
    msg = Message(subject.decode('utf-8'), recipients=[email_to], body=body.decode('utf-8'))
    msg.charset = 'utf-8'
    mail.send(msg)

def send_change_password_email(user_email):
    send_email(
        email_to=user_email,
        subject="Password change",
        body_text="Click the link to change your password: {url}",
        route='profile.change_password'
    )