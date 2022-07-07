from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,login_required,logout_user,current_user
from .models import Tracker
from .models import User
from .models import History
from .models import Log
from . import db
import datetime
current_time = datetime.datetime.now()
views = Blueprint('views',__name__)

@views.route('/',methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html",user=current_user)


@views.route('/update-tracker/<int:id>',methods=['GET', 'POST'])
@login_required
def update_tracker(id):
    present_tracker = Tracker.query.get(id)
    present_tracker_name = present_tracker.name
    if request.method =="POST":
        name = request.form.get("name")
        description = request.form.get("description")
        settings = request.form.get("settings")
        # try something new
        date_time = str(datetime.datetime.utcnow())
        date = date_time[0:10]
        time = date_time[11:19]
        # trysomething new ended

        tracker_user_id = current_user.id
        tracker = Tracker.query.filter_by(name=name).first()
        if tracker:
            if tracker.user_id == tracker_user_id:
                if present_tracker_name !=name:
                    flash("This tracker is already there", category="error")
        else:
            g = "Tracker name: " + present_tracker_name +". " #trysomething new
            if len(name) >0:
                # present_tracker.name = name
                a = " Tracker name is updated: "+ name # try something new
                g = g+a+". " # try something new
                present_tracker.name = name
                db.session.commit()
            if len(description) > 0:
                # present_tracker.description = description
                b = " Tracker description is updated: "+description #try something new
                g=g+b+". " # try something new
                present_tracker.description = description
                db.session.commit()
            if len(settings)>0:
                # present_tracker.settings = settings
                c = " Tracker settings is updated: "+settings #try something new
                g=g+c+". " # try something new
                present_tracker.settings = settings
                db.session.commit()

            # present_tracker.name = name
            # present_tracker.description = description
            # present_tracker.settings = settings

            # db.session.commit()
            flash("Tracker update Successfully", category="success")
            # try something new
            new_history = History(date=date, time=time, user_id=current_user.id, new=g)
            db.session.add(new_history)
            db.session.commit()

            # try something new ended

            return redirect(url_for("views.home"))


    return render_template("update_tracker.html",user=current_user)

@views.route('/log/<int:id>',methods=['GET', 'POST'])
@login_required
def log(id):
    return render_template("log.html",id=id,user=current_user)
@views.route('/history' ,methods=['GET', 'POST'])
@login_required
def history():
    return render_template("history.html",user=current_user)

@views.route('/add_log/<int:id>',methods=['GET', 'POST'])
@login_required
def add_log(id):
    user = current_user
    if request.method == "POST":
        notes = request.form.get("notes")
        print(notes)
        date_time = str(datetime.datetime.utcnow())
        date = date_time[0:10]
        time = date_time[11:19]
        for tracker in user.tracker:
            if tracker.tracker_type == "Multiple Choice" and tracker.id == id:
                a = tracker.name #try something new
                value = request.form.get("Multiple")
                print(value)
            elif tracker.tracker_type =="Text" and tracker.id == id:
                a = tracker.name  # try something new
                value = request.form.get("Text")
                print(value)
            elif tracker.tracker_type=="Numerical" and tracker.id == id:
                a = tracker.name  # try something new
                value = request.form.get("Numerical")
                print(value)
            elif tracker.tracker_type=="Boolean" and tracker.id == id:
                a = tracker.name  # try something new
                value = request.form.get("Boolean")
                print(value)

        new_log = Log(notes=notes, value=value, date=date, time=time, tracker_id=id, user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        print("done")
        flash("Log Added successfully", category="success")
        # try something new
        g = "Log is added in "+a
        new_history = History(date=date, time=time, user_id=current_user.id, new=g)
        db.session.add(new_history)
        db.session.commit()
        # try something new is ended
        return render_template("log.html",id=id,user=current_user)
    for tracker in user.tracker :
        if tracker.tracker_type == "Multiple Choice" and tracker.id == id :
            y = tracker.settings
            x = y.split(",")
            print(x)
            return render_template("add_log.html",id=id,user = current_user,option=x)
    return render_template("add_log.html",id=id,user=current_user)

@views.route('/delete-log/<int:id>',methods=['GET', 'POST'])
@login_required
def log_delete(id):
    user = current_user #something new
    delete_log = Log.query.get(id)
    tracker = delete_log.tracker_id
    db.session.delete(delete_log)
    db.session.commit()
    flash("Log deleted successfully",category="success")
    # try something new
    date_time = str(datetime.datetime.utcnow())
    date = date_time[0:10]
    time = date_time[11:19]
    for x in user.tracker:
        if x.id == tracker:
            tracker_name = x.name
    g = "Log is deleted form  " + tracker_name
    new_history = History(date=date, time=time, user_id=current_user.id, new=g)
    db.session.add(new_history)
    db.session.commit()
    # try something new is endend
    return render_template("log.html", id=tracker , user=current_user)

@views.route('/update-log/<int:id>',methods=['GET', 'POST'])
@login_required
def update_log(id):
    # id tracker ki hai
    print(id)
    present_log = Log.query.get(id)
    tracker_id = present_log.tracker_id
    print(present_log,"present_log")
    print(tracker_id,"tracker_id")
    user = current_user
    if request.method == "POST":
        for tracker in user.tracker:
            if tracker.id == tracker_id :
                if tracker.tracker_type == "Numerical":
                    a = tracker.name #trysomething new
                    print("Numerical")
                    value = request.form.get("Numerical")
                    if value != "":
                        present_log.value = value
                        db.session.commit()
                elif tracker.tracker_type == "Boolean":
                    a = tracker.name  # trysomething new
                    print("Boolean")
                    value = request.form.get("Boolean")
                    present_log.value = value
                    db.session.commit()
                elif tracker.tracker_type == "Text":
                    a = tracker.name  # trysomething new
                    print("text")
                    value = request.form.get("Text")
                    if value != "" :
                        present_log.value = value
                        db.session.commit()

                else:
                    print("value")
                    a = tracker.name  # trysomething new
                    value = request.form.get("Multiple")
                    present_log.value = value
                    db.session.commit()
        dates = request.form.get("date")  # string
        if dates != "":
            present_log.date = dates
            db.session.commit()
        times = request.form.get("time")  # string
        if times != "":
            time = times + ":00"
            present_log.time = time
            db.session.commit()
        notes = request.form.get("notes")  # string
        if notes != "":
            present_log.notes = notes
            db.session.commit()
        flash("Update log Successfully",category="success")
        # try something new
        date_time = str(datetime.datetime.utcnow())
        date = date_time[0:10]
        time = date_time[11:19]
        g = "Log is updated in " +a
        new_history = History(date=date, time=time, user_id=current_user.id, new=g)
        db.session.add(new_history)
        db.session.commit()
        # try something new ended
        return render_template("log.html",id = tracker_id,user=current_user)


    for tracker in user.tracker :
        if tracker.tracker_type == "Multiple Choice" and tracker.id == tracker_id :
            y = tracker.settings
            x = y.split(",")
            print(x)
            return render_template("update_log.html",id=tracker_id,user = current_user,option=x)
    return render_template("update_log.html",id=tracker_id,user=current_user)