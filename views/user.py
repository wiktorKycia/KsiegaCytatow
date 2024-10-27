from flask import Blueprint, render_template, request, redirect, url_for, abort, session, g
from config import mysql, send_change_password_email
from flask_mysqldb import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
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
# TODO: change nickname preferences
# TODO: display favourite quotes

# Route to display the user profile
@profile.route('/')
def user_profile():
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT trust_level, email FROM users WHERE name = %s', (user['name'],))
            trust, email = cursor.fetchone()
            cursor.close()
            if trust < 1:
                session['user_email'] = email
                return render_template("profile/index.html", username=user['name'], canverify=True)

            return render_template("profile/index.html", username=user['name'], canverify=False)
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))

@profile.route('/send_email')
def send_email():
    email = session.get('user_email')
    send_change_password_email(email)
    session.pop('user_email', None)
    return "Check your email inbox for a link"

@profile.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner

            if request.method == 'GET':
                return render_template("profile/change_password.html", password_not_match=False)
            elif request.method == 'POST':
                password = request.form['password']
                password_confirm = request.form['password2']
                if password != password_confirm:
                    return render_template("profile/change_password.html", password_not_match=True)
                else:
                    password = generate_password_hash(password)
                    cursor = mysql.connection.cursor()
                    cursor.execute('UPDATE users SET user_password = %s WHERE name = %s', (password, user['name']))
                    mysql.connection.commit()
                    cursor.close()
                    return redirect(url_for('profile.user_profile', user_url_slug=session['user']), code=302)
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))