from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Workout, User

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@main.route("/new")
@login_required
def new_workout():
    return render_template("create_workout.html")

@main.route("/new", methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form['pushups']
    comment = request.form['comment']

    new_entry = Workout(pushups=pushups, comment=comment, author=current_user)
    db.session.add(new_entry)
    db.session.commit()

    flash("Your workout has been added!")

    return redirect(url_for("main.user_workouts"))

@main.route("/all")
@login_required
def user_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workout = user.workouts
    return render_template("all_workouts.html", workout=workout, user=user)