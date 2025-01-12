from app import app
import app.backend.backend as b
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    user = {"username":"Ram"}
    return render_template("index.html", good="OWIEJFOWEJIEFOWEJI", user=user)
