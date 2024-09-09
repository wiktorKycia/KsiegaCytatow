# Imports
from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == 'GET':
        return render_template('home/login.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT name, email, user_password FROM users 
        WHERE (name=%s OR email=%s) AND user_password=%s''',
        (request.form['username'], request.form['username'], request.form['password']))
        users = cursor.fetchall()
        cursor.close()
        print(users)
        print(type(users))
        return f"{users} <br/> {type(users)}"


# this is only a temporary route, it should be moved to /admin/database/users
@home.route('/database')
def database():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('home/data.html', data=users)