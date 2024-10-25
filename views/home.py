# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session, current_app
from config import mysql, mail
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
# Parent route
home = Blueprint('home', __name__)

# TODO: quick quote add -> admin or moderator has to approve it
# TODO: 3 most liked quotes before register
# TODO: IsUserZSKStudent test in register form
# TODO: add quote
# TODO: search quotes (searchbox)
# TODO: liking quotes

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
    print(user_email)
    token = generate_verification_token(user_email)
    verification_url = url_for('home.verify_email', token=token, _external=True)
    subject = "Please verify your email".encode('utf-8')
    body = f"Click the link to verify your email: {verification_url}".encode('utf-8')

    # Send the email
    msg = Message(subject=subject.decode('utf-8'), recipients=[user_email], body=body.decode('utf-8'))
    msg.charset = 'utf-8'  # Set the encoding explicitly
    print(msg)
    mail.send(msg)

# Routes
@home.route('/')
def homepage():
    """
    The first page that the user sees when entering an app
    :return: html
    """
    return render_template('home/index.html', title='Home', content='home')

@home.route('/login', methods=['GET', 'POST'])
def login():
    # the user enters the /login by the link in browser
    if request.method == 'GET':
        # if the user is already logged in, push him back to his user page
        if "user" in session:
            return redirect(url_for('profile.user_profile', user_url_slug=session['user']))
        return render_template('home/login.html')
    # user fills out the form and clicks submit
    elif request.method == 'POST':
        # connect to the database
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT name, email, user_password FROM users 
        WHERE (name=%s OR email=%s) AND user_password=%s''',
        (request.form['username'], request.form['username'], request.form['password']))
        # save the results from the database
        users:tuple[tuple[str, str, str]] = cursor.fetchall()
        cursor.close()
        if not users:
            return redirect(url_for('home.login'))
        # if the database would somehow return 2 rows instead of 1
        if len(users) > 1:
            return abort(500)
        else:
            # start the session and redirect to userhomepage
            session.permanent = True
            user = users[0]
            session['user'] = user[0]
            return redirect(url_for('profile.user_profile', user_url_slug=user[0]))


@home.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home.login"))


@home.route('/register/', methods=['GET'])
def register():
    email = session.get('user_email')
    send_verification_email(email)
    session.pop('user_email', None)
    return "Check your email inbox for a verification link."


@home.route('/verify/<token>')
def verify_email(token):
    try:
        email = verify_token(token)
    except:
        print('The verification link is invalid or has expired.')
        # flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))

    # Update the user's trust level in the database
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET trust_level = 2 WHERE email = %s", (email,))
    mysql.connection.commit()
    cursor.close()

    print('Your account has been verified!')
    # flash('Your account has been verified!', 'success')
    return redirect(url_for('home.login'))