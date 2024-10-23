# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql
from itsdangerous import URLSafeTimedSerializer
# Parent route
home = Blueprint('home', __name__)

# TODO: quick quote add -> admin or moderator has to approve it
# TODO: 3 most liked quotes before register
# TODO: IsUserZSKStudent test in register form
# TODO: add quote
# TODO: search quotes (searchbox)
# TODO: liking quotes

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


@home.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        email = request.form['email']
        # Other registration logic...

        send_verification_email(email)
        print('A verification email has been sent to your inbox.')
        # flash('A verification email has been sent to your inbox.', 'info')
        return redirect(url_for('home.login'))
