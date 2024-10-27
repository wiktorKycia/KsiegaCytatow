from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from flask import current_app, url_for, render_template
from itsdangerous import URLSafeTimedSerializer

mysql = MySQL()
mail = Mail()

def generate_verification_token(email):
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