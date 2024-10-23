from flask import Blueprint, render_template, request, redirect, url_for, abort, session, g
from config import mysql
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


    if "user" in session:
        g.profile_owner = user  # Store the user info in the 'g' object
    else:
        return redirect(url_for("home.login"))


# TODO: enable user to change password
# TODO: email verification
# TODO: change nickname preferences
# TODO: display favourite quotes

# Route to display the user profile
@profile.route('/')
def user_profile():
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT trust_level FROM users WHERE name = %s', (user,))
            trust = cursor.fetchone()[0]
            cursor.close()
            if trust < 1:
                return render_template("profile/index.html", username=user['name'], canverify=True)

            return render_template("profile/index.html", username=user['name'], canverify=True)
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))