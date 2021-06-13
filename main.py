# base packages

# PyPi packages
from flask import render_template

# custom methods and classes
from models import *


@app.route('/')
def splash():
    """
    Splash page for user.
    """
    return render_template('splash.html', title="Gift Gopher")


@app.route('/login')
def login():
    return "login page."


@app.route('/signup')
def signup():
    return "Signup page."


if __name__ == "__main__":
    app.run(
        debug=True
    )