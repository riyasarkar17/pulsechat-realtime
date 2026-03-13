from __future__ import annotations

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins='*')
