# base packages

# PyPi packages
from flask import render_template, redirect, url_for, flash, request, g
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import NoResultFound

# custom packages
from models import User, Gifts, app, db, bcrypt, login_manager
from forms import RegistrationForm, LoginForm, CreateGiftForm
from custom_exceptions import IncorrectPassword

# Global Variables
WEBSITE_NAME = "Gift Gopher"


######################################################################
#                       helper functions
######################################################################

def trylogin(form: LoginForm) -> str:
    """
    Try to login. Returns empty string
    :param form: LoginForm
    :return str for where to redirect next.
    """

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


######################################################################
#                       search functions
######################################################################

# search handler
@app.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('splash'))
    return redirect(url_for('search_results', qry=g.search_form.search.data))

@app.route('/search/<qry>', methods=['POST', 'GET'])
def search_results(qry):
    raw_qry = qry
    qry = raw_qry.strip()
    qry = "%{}%".format(qry)
    if qry:
        gift_results = db.session.query(Gifts).filter(
            Gifts.name.ilike(qry)
        ).limit(50).all()
    else:
        gift_results = []

    return render_template('results.html', qry=raw_qry, gift_results=gift_results)


######################################################################
#                       base functionality
######################################################################

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
            return redirect(url_for(next_path))

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


######################################################################
#                       gifts
######################################################################


@app.route('/user/<username>/gifts/add', methods=['GET', 'POST'])
@login_required
def gifts_add(username):
    form = CreateGiftForm()

    if form.validate_on_submit():
        _gifts_add(form)

        return redirect(url_for('gifts_add', username=current_user.username))

    return render_template('gifts_add.html', title='Add Gift', form=form)


######################################################################
#                       profile
######################################################################


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


if __name__ == "__main__":
    app.run(
        debug=True
    )
