from flask import Flask
from config import Config
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, logger=True, engineio_logger=True)

from app import routes
