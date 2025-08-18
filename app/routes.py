from urllib.parse import urlsplit
from itsdangerous import url_safe
from app import app, socketio, db
from flask import render_template, flash, redirect, request, url_for, session
from app.forms import LoginForm, RegisterForm
from flask_socketio import emit, join_room, leave_room
import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_login import login_required, login_user, current_user, logout_user
from app.models import ActiveUsers, Chats, Messages, User

# We have refactor this code to split this code up into different blueprints

@app.route("/")
@app.route("/index")
@login_required
def index():
    chats_id = []
    chats_name = []
    chats = db.session.scalars(sa.select(Chats)).all()
    for chat in chats:
        if not current_user in chat.users:
            continue
        chats_id.append(str(chat.id))
        if not chat.name:
            temp_name = createTempChatName(chat.users)
            chats_name.append(temp_name)
            chat.name = temp_name
        else:
            chats_name.append(chat.name)
        db.session.commit()
        db.session.flush()

    return render_template("index.html", chats_id=chats_id, chats_name=chats_name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/createChat", methods=["GET", "POST"])
@login_required
def chatCreator():
    if request.method == "POST":
        users_str = request.form.get("users")
        name = request.form.get("name")
        if not users_str or not name:
            return render_template("create-chat.html")
        users = users_str.split(",")
        createChat(users=users, name=name)
        return redirect(url_for("index"))
    return render_template("create-chat.html")

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

    print(f"Connected on server end, with connection id being {request.sid}")


@socketio.event
def disconnect():
    with orm.Session(db.engine) as s:
        select_stmt = sa.select(ActiveUsers).where(ActiveUsers.user_id == current_user.id)
        u = s.scalar(select_stmt)
        if u:
            s.delete(u)
            s.commit()

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

        message = Messages(chat=chat, text=data["message"], author_id=current_user.id)
        s.add(message)
        s.commit()

@socketio.on("requestUserName")
def requestUserName():
    emit("getUserName", {"username": current_user.username})

@socketio.on("changeChatName")
def changeChatName(data):
    chat = db.session.scalar(sa.select(Chats).where(Chats.id == data["chat_id"]))
    if not chat:
        return
    chat.name = data["new_chat_name"]
    db.session.commit()

@socketio.on("joinChat")
def joinChat(data):
    chat = db.session.get(Chats, int(data["new_room"]))
    if not current_user.is_authenticated or not chat:
        return
    if session["current_room"]:
        leave_room(session["current_room"])
    session["current_room"] = data["new_room"]
    join_room(session["current_room"])

    authors = []
    text = []
    for message in chat.messages:
        authors.append(message.author.username)
        text.append(message.text)
    emit("getMessages", {"authors": authors, "text": text})

def createChat(users: list[str], name: str) -> None:
    if not current_user.username in users:
        users.append(current_user.username)

    chats_users: list[User] = []

    for username in users:
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if not user:
            print(f"this guys isnt a real users lmao {username}")
            return
        chats_users.append(user)

    if not name:
        name = createTempChatName(users=chats_users)
    new_chat = Chats(users=chats_users, name=name)
    db.session.add(new_chat)
    db.session.commit()

    # Tried to update it in real time, but didn't work, will try again tomorrow
    # for user in chats_users:
    #     connection_id = db.session.scalar(sa.select(ActiveUsers).where(ActiveUsers.user_id == user.id))
    #     socketio.emit("addChat", {"chat_id": new_chat.id, "chat_name": new_chat.name})

def createTempChatName(users: list[User]) -> str:
    answer = ""
    for user in users:
        answer += f", {user.username}"

    return answer[2:]
