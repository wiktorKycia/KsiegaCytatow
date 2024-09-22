# Imports
from flask import Flask, render_template, redirect, url_for

from views import user
from views.home import home
from views.admin import admin
from views.user import profile
from db import mysql
from secrets import token_hex
from datetime import timedelta

# Main app
app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ksiegacytatow'

mysql.init_app(app)

# no need for db.py
# mysql = MySQL(app)
# app.mysql = mysql  # Make `mysql` accessible via `current_app`
# then in views: from flask_mysqldb import MySQLdb, current_app

# Session config
app.config['SECRET_KEY'] = token_hex(32)
app.permanent_session_lifetime = timedelta(days=1)

# Blueprints
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(profile, url_prefix='/<user_url_slug>')

# Main route
@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

# Run
if __name__ == '__main__':
    with app.app_context():
        app.run()
