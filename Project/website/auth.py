from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import Tracker
from .models import Log
from .models import History
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import datetime
current_time = datetime.datetime.now()


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,last_name=last_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/add-tracker', methods=['GET', 'POST'])
@login_required
def add_tracker():
    if request.method == 'POST':
        name = request.form.get('name')
        tracker_type = request.form.get('type')
        description = request.form.get('description')
        settings = request.form.get('settings')
        date_time = str(datetime.datetime.utcnow())
        date = date_time[0:10]
        time = date_time[11:19]

        du = Tracker.query.filter_by(name=name).first()
        if du:
            flash('Tracker already exists.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif len(tracker_type) < 2:
            flash('Tracker type name must be greater than 1 character.', category='error')
        elif len(description) < 2:
            flash('Description must be greater than 1 character.', category='error')
        else:
            new_tracker = Tracker(name = name,tracker_type=tracker_type,description=description,date=date,time=time,settings=settings,user_id=current_user.id)
            db.session.add(new_tracker)
            db.session.commit()
            flash('Tracker is created', category='success')
            # try something new
            g = name+" tracker is created."
            new_history = History(date=date, time=time, user_id=current_user.id, new=g)
            db.session.add(new_history)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("add_trackers.html", user=current_user)

@auth.route("/delete_tracker/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_tracker(id):
    data = Tracker.query.get(id)
    # try something new
    name = data.name
    date_time = str(datetime.datetime.utcnow())
    date = date_time[0:10]
    time = date_time[11:19]
    # try something new added
    log = data.log
    if log:
        print("Yes there is a log")
        for x in log:
            print(log)
            db.session.delete(x)
            db.session.commit()
    db.session.delete(data)
    db.session.commit()
    flash("Tracker Deleted Successfully.", category="success")
    # try something new
    g=name+" tracker is deleted."
    new_history = History(date=date, time=time, user_id=current_user.id, new=g)
    db.session.add(new_history)
    db.session.commit()
    #try somethinf new is ended


    return redirect(url_for("views.home"))

