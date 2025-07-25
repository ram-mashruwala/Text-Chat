from urllib.parse import urlsplit
from app import app, socketio
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegisterForm
from flask_socketio import emit
import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_login import login_required, login_user, current_user, logout_user
from app import db
from app.models import User

@app.route("/")
@app.route("/index")
@login_required
def index():
    with orm.Session(db.engine) as session:
        select_stmt = sa.select(User.username).where(User.username != current_user.username)
        temp_users = session.execute(select_stmt).all()
        users = []
        for r in temp_users:
            users.append(r.username)
        print(users)
    return render_template("index.html", users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        select_stmt = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalar(select_stmt)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "" or next_page == "/":
            return redirect(url_for("index"))
        return redirect(url_for(next_page[1:]))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        socketio.emit("addChat", {"username": form.username.data})
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/terms-and-conditions")
def termsAndConditions():
    return render_template("terms.html")

@socketio.event
def connect(auth):
    print(f"Connected on server end, with connection id being {request.sid}")

@socketio.event
def disconnect():
    print(f"Disconnected on server end, with connection id being {request.sid}")

@socketio.on("message")
def message(data):
    emit("message", {"message": data["message"], "author": current_user.username}, broadcast=True, include_self=False)
