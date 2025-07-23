from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, logger=True, engineio_logger=True)


class Base(DeclarativeBase): pass
db = SQLAlchemy(model_class=Base, app=app)
migrate = Migrate(app, db)



from app import routes, models
