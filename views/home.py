# Imports
from flask import Blueprint, render_template
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


# this is only a temporary route, it should be moved to /admin/database/users
@home.route('/database')
def database():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('home/data.html', data=users)