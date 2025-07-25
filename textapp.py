from app import app, socketio, db
import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models import ActiveUsers, User, Messages, Chats

@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "orm": orm, "db": db, "User": User, "Messages": Messages, "Chats": Chats, "ActiveUsers": ActiveUsers}

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", ssl_context="adhoc")
