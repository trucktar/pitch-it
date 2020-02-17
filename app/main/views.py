import json

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PitchForm
from app.models import Pitch, User


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@bp.route("/pitches", methods=["GET", "POST"])
@bp.route("/pitches/<category>", methods=["GET", "POST"])
@login_required  # redirect to login view if user not active
def pitches(category=None):
    form = PitchForm()
    if form.validate_on_submit():
        content = Pitch(
            category=form.category.data, content=form.content.data, user=current_user
        )

        db.session.add(content)
        db.session.commit()

        flash("Your pitch is now live!")
        return redirect(url_for("main.pitches"))

    if not category:
        pitches = Pitch.query.order_by(Pitch.timestamp.desc())
    else:
        pitches = Pitch.query.filter_by(category=category).order_by(
            Pitch.timestamp.desc()
        )

    return render_template("index.html", title="Home", form=form, pitches=pitches)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    pitches = Pitch.query.filter_by(user=current_user).order_by(Pitch.timestamp.desc())

    return render_template("main/user.html", user=user, pitches=pitches)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data

        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.about.data = current_user.about

    return render_template("main/edit_profile.html", title="Edit Profile", form=form)


@bp.route("/upvote", methods=["POST"])
def upvote_post():
    if request.method == "POST":
        data_received = json.loads(request.data)
        print(data_received)

        pitch = Pitch.query.filter_by(id=data_received["postid"]).first()
        print(pitch)

        if pitch:
            setattr(pitch, "upvotes", pitch.upvotes + 1)
            db.session.commit()

            return json.dumps({"upvotes": pitch.upvotes})
    return redirect(url_for("main.pitches"))


@bp.route("/downvote", methods=["POST"])
def downvote_post():
    if request.method == "POST":
        data_received = json.loads(request.data)

        pitch = Pitch.query.filter_by(id=data_received["postid"]).first()

        if pitch:
            setattr(pitch, "downvotes", pitch.downvotes + 1)
            db.session.commit()

            return json.dumps({"downvotes": pitch.downvotes})
    return redirect(url_for("main.pitches"))

