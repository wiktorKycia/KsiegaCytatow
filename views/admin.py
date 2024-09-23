# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql
from flask_mysqldb import MySQLdb

# Parent route
admin = Blueprint('admin', __name__)

# To all routes in admin:
# TODO: when admin is not logged in redirect to login (or admin)

# TODO: To routes: /quotes, /authors, /nicknames -> make html templates for those
# TODO: to routes: /quotes, /authors, /nicknames, /users/ -> only user of trust_level of 3 can see these

# Routes
@admin.route('/')
def admin_home_page():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            return render_template('admin/index.html')
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))
@admin.route('/quotes')
def admin_quotes():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            cursor = mysql.connection.cursor()
            cursor.execute("""
            SELECT q.id, q.content, q.date, q.context, CONCAT(a.first_name, a.middle_name, a.last_name) AS 'author name'
            FROM quotes q
            LEFT OUTER JOIN authors a ON q.author_id = a.id""")
            quotes = cursor.fetchall()
            cursor.execute("DESCRIBE quotes")
            columns = cursor.fetchall()
            cursor.close()
            return render_template("admin/quotes.html", data=quotes, columns=columns)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))


@admin.route('/users/')
def admin_users():
    if "user" in session:
        if session['user'] == "admin":
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            cursor.execute('DESCRIBE users')
            columns = cursor.fetchall()
            cursor.close()
            return render_template("admin/users.html", data=users, columns=columns)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/users/<user>')
def admin_user_detail(user):
    if "user" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = %s', (session['user'],))
        usr = cursor.fetchone()
        cursor.close()
        print(usr)
        if usr['name'] == "admin" and session['user'] == "admin":
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM users WHERE name = %s''', (user,))
            user_data = cursor.fetchone()
            cursor.close()
            return render_template("admin/user.html", user=user_data)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/nicknames')
def admin_nicknames():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            return "list of nicknames here, with full access to add, modify, delete and update"
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/nicknames/<author_id>')
def admin_nickname(author_id):
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            cursor = mysql.connection.cursor()
            cursor.execute("""
            SELECT CONCAT(a.first_name, a.middle_name, a.last_name) AS 'author name', 
            FROM authors WHERE id = %s""", (author_id,))
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))
# TODO: in authors.html provide a link to a route that will grab the author's id, select the data from database
# and redirect to nicknames/<author_id>
@admin.route('/authors')
def admin_authors():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM authors")
            authors = cursor.fetchall()
            cursor.execute("DESCRIBE authors")
            columns = cursor.fetchall()
            cursor.close()
            return render_template("admin/authors.html", data=authors, columns=columns)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/database', methods=['GET', 'POST'])
def admin_database():
    if request.method == 'GET':
        if "user" in session:
            if session["user"] == "admin":
                return render_template("admin/database.html", data=None, query_value="")
            else:
                abort(403)
        else:
            return redirect(url_for('home.login'))
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(request.form['query'])
        data = cursor.fetchall()
        cursor.close()
        return render_template("admin/database.html", data=data, query_value=request.form['query'])