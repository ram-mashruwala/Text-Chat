from app import app, socketio
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegisterForm
from flask_socketio import emit
import sqlalchemy as sa
from flask_login import login_user, current_user, logout_user
from app import db
from app.models import User

@app.route("/")
@app.route("/index")
def index():
    return render_template("template.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        redirect(url_for("template"))
    form = LoginForm()
    if form.validate_on_submit():
        select_stmt = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalar(select_stmt)
        if user is None or not user.check_password(str(form.password.data)):
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("template"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/terms-and-conditions")
def termsAndConditions():
    return render_template("terms.html")

@socketio.event
def connect(auth):
    print(f"Connected on server end, with connection id being {request.sid}")

@socketio.event
def disconnect():
    print(f"Disconnected on server end, with connection id being {request.sid}")
    logout_user()

@socketio.on("message")
def message(data):
    emit("message", {"message": data["message"], "author": session["username"]}, broadcast=True, include_self=False)

@socketio.on("setUserName")
def getUserName(data):
    session["username"] = data["username"]
