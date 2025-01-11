from app import app
import app.backend.backend as b

@app.route("/")
@app.route("/index")
def index():
    return f"hello there {b.main()}"
