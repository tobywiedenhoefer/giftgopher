# base packages

# PyPi packages
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import NoResultFound

# custom packages
from models import *
from forms import *
from custom_exceptions import IncorrectPassword

# Global Variables
WEBSITE_NAME = "Gift Gopher"


def trylogin(form: LoginForm) -> str:
    """
    Try to login. Returns empty string
    :param form: LoginForm
    :return str for where to redirect next.
    """

    # TODO: log login tries
    try:
        user = User.query.filter_by(username=form.username.data).one()  # throws NoResultFound if username not found.
        if not bcrypt.check_password_hash(user.password, form.password.data):
            raise IncorrectPassword
    except NoResultFound:
        flash('Login unsuccessful. Check your username and password.', 'danger')
        return ""
    except IncorrectPassword:
        flash('Login unsuccessful. Check your username and password.', 'danger')
        return ""

    login_user(user=user, remember=form.remember.data)

    next_path = request.args.get('next')  # /login?next=next_path
    print(next_path)

    if next_path:
        if next_path[0] == "/":
            next_path = next_path[1::]
        return next_path
    return 'splash'


@app.route('/')
def splash():
    """
    Splash page for user.
    """
    return render_template('splash.html', title=WEBSITE_NAME)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('splash'))

    form = LoginForm()

    if form.validate_on_submit():

        next_path = trylogin(form)

        if next_path:
            return  redirect(url_for(next_path))

    return render_template('login.html', title='Log In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('splash'))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_pass = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pass, email=form.email.data)

        db.session.add(user)
        db.session.commit()

        flash('Account created! Please sign in.')

        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('splash'))


if __name__ == "__main__":
    '''app.run(
        debug=True
    )'''
    users = User.query.all()
    for user in users:
        print(user.id, user.username, user.email)