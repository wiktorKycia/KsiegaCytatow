# Imports
from flask import Flask, render_template, redirect, url_for
from views.home import home
from views.admin import admin
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

# Session config
app.config['SECRET_KEY'] = token_hex(32)
app.permanent_session_lifetime = timedelta(days=1)

# Blueprints
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(admin, url_prefix='/admin')

# Main route
@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

# Run
if __name__ == '__main__':
    app.run()
