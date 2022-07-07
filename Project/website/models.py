from . import db
from flask_login import UserMixin
from datetime import date,datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    timeStamp_user = db.Column(db.DateTime, default=datetime.utcnow())
    tracker = db.relationship('Tracker')
    log = db.relationship('Log')
    history = db.relationship('History')


class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    tracker_type = db.Column(db.String(200))
    settings = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    # newly added
    # date = db.Column(db.Date,defaut=datetime.date())
    # time = db.Column(db.DateTime,default=datetime.utcnow())
    # close
    timeStamp_tracker = db.Column(db.DateTime,default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    log = db.relationship('Log')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # value = db.Column(db.Integer)
    value = db.Column(db.String(150))
    notes = db.Column(db.String(150))
    # value,notes for user
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    timeStamp_log = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    new = db.Column(db.String(100))
    timeStamp_log = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

