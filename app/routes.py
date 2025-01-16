from app import app
import app.backend.backend as b
from flask import render_template, flash, redirect
import app.backend.User as user
from app.backend.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("template.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect("/index")
    return render_template("login.html", title="Ram", form=form)
