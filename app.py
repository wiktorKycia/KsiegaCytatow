# Imports
from flask import Flask, render_template, redirect, url_for

from views import user
from views.home import home
from views.admin import admin
from views.user import profile
from db import mysql
from secrets import token_hex
from datetime import timedelta

import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()
# Main app
app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ksiegacytatow'

mysql.init_app(app)

# Mail config
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Using security salt for token generation
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')

mail = Mail(app)

# no need for db.py
# mysql = MySQL(app)
# app.mysql = mysql  # Make `mysql` accessible via `current_app`
# then in views: from flask_mysqldb import MySQLdb, current_app

# Session config
app.config['SECRET_KEY'] = token_hex(32)
app.permanent_session_lifetime = timedelta(days=1)

# Blueprints
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(profile, url_prefix='/profile/<user_url_slug>')

from itsdangerous import URLSafeTimedSerializer
# TODO: point 3 of GPT prompt, move some parts to home.py
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration  # Token expires after 1 hour
        )
    except:
        return False
    return email

def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    verification_url = url_for('verify_email', token=token, _external=True)
    subject = "Please verify your email"
    body = f"Click the link to verify your email: {verification_url}"

    # Send the email
    msg = Message(subject=subject, recipients=[user_email], body=body)
    mail.send(msg)

# Main route
@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

@app.route('/verify/<token>')
def verify_email(token):
    try:
        email = verify_token(token)
    except:
        print('The verification link is invalid or has expired.')
        # flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('home'))

    # Update the user's trust level in the database
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET trust_level = 2 WHERE email = %s", (email,))
    mysql.connection.commit()
    cursor.close()

    print('Your account has been verified!')
    # flash('Your account has been verified!', 'success')
    return redirect(url_for('login'))


# Run
if __name__ == '__main__':
    with app.app_context():
        app.run()
