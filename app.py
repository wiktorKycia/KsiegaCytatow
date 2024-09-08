from flask import Flask, render_template, redirect, url_for
from views.home import home
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ksiegacytatow'
app.register_blueprint(home, url_prefix='/home')

@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

if __name__ == '__main__':
    app.run()
