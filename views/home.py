# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql

# Parent route
home = Blueprint('home', __name__)

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
            return redirect(url_for('home.userhomepage'))
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
        # if the database would somehow return 2 rows instead of 1
        if len(users) > 1:
            return abort(500)
        else:
            # start the session and redirect to userhomepage
            session.permanent = True
            user = users[0]
            session['user'] = user[0]
            return redirect(url_for('home.userhomepage'))

@home.route('/user')
def userhomepage():
    # the user is logged in, so we allow him to view his page
    if "user" in session:
        return render_template('home/user.html', username=session['user'])
    else:
        # the user is not logged in, so we redirect him back to login
        return redirect(url_for('home.login'))

@home.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home.login"))


# this is only a temporary route, it should be moved to /admin/database/users
@home.route('/database')
def database():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('home/data.html', data=users)