# base packages

# PyPi packages
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import NoResultFound

# custom packages
from models import User, Gifts, app, db, bcrypt, login_manager
from forms import RegistrationForm, LoginForm, CreateGiftForm
from custom_exceptions import IncorrectPassword

# Global Variables
WEBSITE_NAME = "Gift Gopher"

# TODO: add activity feed; whenever someone adds a gift, connection, wishlist,


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

    if next_path:
        if next_path[0] == "/":
            next_path = next_path[1::]
        return next_path
    return 'splash'


def _gifts_add(form: CreateGiftForm):
    """
    Helper method to add gifts
    :param form: CreateGiftForm
    """
    gift = Gifts(
        user_id=current_user.id,
        name=form.name.data,
        description=form.description.data,
        link=form.link.data,
        public=form.public.data
    )
    db.session.add(gift)
    db.session.commit()

    flash('Gift created!', 'success')


@app.route('/')
def splash():
    """
    Splash page for user.
    """
    # TODO: add feed to root
    # TODO: once authenticated, change navbar to have pictures/buttons for 'gifts -> add/vew mine/search'
    #  'people -> view/search'
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


@app.route('/user/<username>/gifts/add', methods=['GET', 'POST'])
@login_required
def gifts_add(username):

    form = CreateGiftForm()

    if form.validate_on_submit():

        _gifts_add(form)

        return redirect(url_for('gifts_add'))

    return render_template('gifts_add.html', title='Add Gift', form=form)


@app.route('/user/<username>', methods=['GET', 'POST', 'DELETE'])
@login_required
def profile(username):

    page_user = db.session.query(User).filter_by(username=username).first()

    if not page_user:  # username is not an active username
        return "Throw 404", 404
    elif page_user.id == current_user.id:  # current user is viewing their own page
        gifts = db.session.query(Gifts).filter_by(user_id=current_user.id).all()
        is_owner = True
    else:  # someone else is viewing username's page
        gifts = db.session.query(Gifts).filter_by(user_id=page_user.id, public=True).all()
        is_owner = False

    return render_template(
        'profile.html',
        gifts=gifts,
        title=current_user.username,
        profile_user=username,
        owner=is_owner
    )
# TODO: gifts/view?gift_id=<gift_id>    views
# TODO: gifts/view?update=<gift_id>&update=True     update view loads if author of gift


if __name__ == "__main__":
    app.run(
        debug=True
    )