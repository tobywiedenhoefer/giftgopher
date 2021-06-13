# base packages
from datetime import datetime

# PyPi packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////giftgopher.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    gifts = db.relationship('Gifts', backref='user')
    connections = db.relationship('Connections', backref='user')


class Gifts(db.Model):
    __tablename__ = "gifts"

    gift_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    link = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(140), nullable=True)
    public = db.Column(db.Boolean, nullable=False, default=False)

    holiday = db.relationship('Holidays', backref='gifts')

    def __repr__(self):
        return f"Gift: {self.name}"


class Connections(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    follower_name = db.Column(db.String(15), db.ForeignKey('user.username'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following_name = db.Column(db.String(15), db.ForeignKey('user.usernae', nullable=False))


class Holidays(db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    gift_id = db.Column(db.Integer, db.ForeignKey('gifts.gift_id'), nullable=False)
    holiday = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # TODO: create relationship with Gifts?


db.drop_all()
db.create_all()
