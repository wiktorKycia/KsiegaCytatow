# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql

# Parent route
admin = Blueprint('admin', __name__)

# Routes
@admin.route('/')
def admin_home_page():
    if "user" in session:
        if session["user"] == "admin": # TODO: przerobić na sprawdzenie przez trust level
            return render_template('admin/index.html')
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))
@admin.route('/quotes')
def admin_quotes():
    return "list of quotes here, with full access to add, modify, delete and update"

@admin.route('/users')
def admin_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.execute('DESCRIBE users')
    columns = cursor.fetchall()
    cursor.close()
    return render_template("admin/users.html", data=users, columns=columns)

@admin.route('/nicknames')
def admin_nicknames():
    return "list of nicknames here, with full access to add, modify, delete and update"

@admin.route('/authors')
def admin_authors():
    return "list of authors here, with full access to add, modify, delete and update"