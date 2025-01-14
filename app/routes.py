from app import app
import app.backend.backend as b
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return render_template("template.html")

@app.route("/login")
def login():
    return render_template("login.html")
