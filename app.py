# Imports
from flask import Flask, render_template, redirect, url_for
from views.home import home
from db import mysql

# Main app
app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ksiegacytatow'

mysql.init_app(app)

# Blueprints
app.register_blueprint(home, url_prefix='/home')

# Main route
@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

# Run
if __name__ == '__main__':
    app.run()
