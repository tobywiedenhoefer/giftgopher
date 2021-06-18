# base packages

# PyPi packages
from flask import render_template, redirect, url_for
from flask_login import current_user

# custom methods and classes
from models import *
from forms import *

# Global Variables
WEBSITE_NAME = "Gift Gopher"


@app.route('/')
def splash():
    """
    Splash page for user.
    """
    return render_template('splash.html', title=WEBSITE_NAME)


@app.route('/login')
def login():
    return "login page."


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('splash'))

    form = RegistrationForm()

    if form.validate_on_submit():

        print(
            form.username.data,
            form.email.data
        )

        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run(
        debug=True
    )