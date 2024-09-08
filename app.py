from flask import Flask, render_template, redirect, url_for
from views.home import home
app = Flask(__name__)
app.register_blueprint(home, url_prefix='/home')

@app.route('/')
def index():
    return redirect(url_for('home.homepage'))

if __name__ == '__main__':
    app.run()
