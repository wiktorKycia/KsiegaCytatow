from flask import Blueprint, render_template
from db import mysql
home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    """
    The first page that the user sees when entering an app
    :return: html
    """
    return render_template('home/index.html', title='Home', content='home')

@home.route('/database')
def database():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('home/data.html', data=users)