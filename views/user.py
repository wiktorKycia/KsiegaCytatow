from flask import Blueprint, render_template, request, redirect, url_for, abort, session, g
from db import mysql
from flask_mysqldb import MySQLdb

profile = Blueprint('profile', __name__)


# URL Preprocessor to fetch user by slug
@profile.url_value_preprocessor
def get_profile_owner(endpoint, values):
    user_url_slug = values.pop('user_url_slug')  # Extract the slug from the URL

    # Execute SQL query to fetch the user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM users WHERE name = %s', (user_url_slug,))

    user = cur.fetchone()
    cur.close()

    if user is None:
        return "User not found", 404

    g.profile_owner = user  # Store the user info in the 'g' object


# Route to display the user profile
@profile.route('/')
def user_profile():
    user = g.profile_owner  # Get the user from the preprocessor
    # return render_template('profile.html', user=user)
    return f'this is {user}' # TODO: template for user profile page