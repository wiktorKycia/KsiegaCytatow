from flask import Flask, render_template, redirect, url_for
from views.home import home as home_blueprint
app = Flask(__name__)
app.register_blueprint(home_blueprint, url_prefix='/home')

@app.route('/')
def index():
    return redirect(url_for('home_blueprint.home'))


if __name__ == '__main__':
    app.run()
