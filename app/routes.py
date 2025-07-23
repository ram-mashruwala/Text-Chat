from app import app, socketio
from flask import render_template, flash, redirect, request, session
from app.forms import LoginForm, RegisterForm
from flask_socketio import emit


@app.route("/")
@app.route("/index")
def index():
    return render_template("template.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Ram", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect("/index")
    return render_template("register.html", title="Register", form=form)

@socketio.event
def connect(auth):
    print(f"Connected on server end, with connection id being {request.sid}")

@socketio.event
def disconnect():
    print(f"Disconnected on server end, with connection id being {request.sid}")

@socketio.on("message")
def message(data):
    print(session["username"])
    emit("message", {"message": data["message"], "author": session["username"]}, broadcast=True, include_self=False)
    print(data)

@socketio.on("setUserName")
def getUserName(data):
    session["username"] = data["username"]
    print(session["username"])
