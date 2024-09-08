from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('home/'))


if __name__ == '__main__':
    app.run()
