# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session, current_app
from config import mysql, mail, send_verification_email, verify_token
from werkzeug.security import generate_password_hash, check_password_hash

# Parent route
home = Blueprint('home', __name__)

# TODO: quick quote add -> admin or moderator has to approve it
# TODO: 3 most liked quotes before register
# TODO: IsUserZSKStudent test in register form
# TODO: add quote
# TODO: search quotes (searchbox)
# TODO: liking quotes



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
        WHERE (name=%s OR email=%s)''',
        (request.form['username'], request.form['username']))
        # save the results from the database
        users:tuple[tuple[str, str, str]] = cursor.fetchall()
        cursor.close()
        if not users:
            return redirect(url_for('home.login'))
        # if the database would somehow return 2 rows instead of 1
        if len(users) > 1:
            return abort(500)
        else:
            user = users[0]
            hashed_password = generate_password_hash(request.form['password'])
            if check_password_hash(user[0][2], hashed_password):
                # start the session and redirect to userhomepage
                session.permanent = True
                session['user'] = user[0]
                return redirect(url_for('profile.user_profile', user_url_slug=user[0]))
            else:
                return redirect(url_for('home.login'))


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