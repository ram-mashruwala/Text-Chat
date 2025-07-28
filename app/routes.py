from typing import List
from urllib.parse import urlsplit
from app import app, socketio
from flask import render_template, flash, redirect, request, url_for, session
from app.forms import LoginForm, RegisterForm
from flask_socketio import emit, join_room, leave_room
import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_login import login_required, login_user, current_user, logout_user
from app import db
from app.models import ActiveUsers, Chats, Messages, User

@app.route("/")
@app.route("/index")
@login_required
def index():
    chats_id = []
    chats_name = []
    with orm.Session(db.engine) as s:
        select_stmt = sa.select(Chats)
        chats = s.execute(select_stmt)
        for c in chats:
            if not current_user in c[0].users:
                continue

            chats_id.append(str(c[0].id))
            if not c[0].name:
                temp_name = createTempChatName(c[0].users)
                chats_name.append(temp_name)
                c[0].name = temp_name
                s.commit()
            else:
                chats_name.append(c[0].name)

    return render_template("index.html", chats_id=chats_id, chats_name=chats_name)

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
        session["current_room"] = None
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
    with orm.Session(db.engine) as s:
        select_stmt = sa.select(ActiveUsers).where(ActiveUsers.user_id == current_user.id)
        user = s.execute(select_stmt).first()
        if not user:
            active_user = ActiveUsers(connection_id=request.sid, user_id=current_user.id)
            s.add(active_user)
            s.commit()
            s.flush()

    print(f"Connected on server end, with connection id being {request.sid}")


@socketio.event
def disconnect():
    with orm.Session(db.engine) as s:
        select_stmt = sa.select(ActiveUsers).where(ActiveUsers.user_id == current_user.id)
        u = s.scalar(select_stmt)
        if u:
            s.delete(u)
            s.commit()
            s.flush()

    print(f"Disconnected on server end, with connection id being {request.sid}")

@socketio.on("message")
def message(data):
    if not session["current_room"]:
        return
    emit("message",
         {"message": data["message"], "author": current_user.username},
         include_self=False,
         room=session["current_room"])
    with orm.Session(db.engine) as s:
        select_stmt = sa.select(Chats).where(Chats.id == int(session["current_room"]))
        chat = s.scalar(select_stmt)
        if not chat:
            return

        if not chat.messages:
            chat.messages = []
        message = Messages(chat=chat, text=data["message"], author_id=current_user.id)
        s.add(message)
        s.commit()
        s.flush()

@socketio.on("requestUserName")
def requestUserName():
    emit("getUserName", {"username": current_user.username})




@socketio.on("joinChat")
def joinChat(data):
    if not current_user.is_authenticated:
        return
    if session["current_room"]:
        leave_room(session["current_room"])
    session["current_room"] = data["new_room"]
    join_room(session["current_room"])


def createTempChatName(users: List[User]) -> str:
    answer = users[0].username
    for user in users[1:]:
        answer += f", {user.username}"

    return answer

