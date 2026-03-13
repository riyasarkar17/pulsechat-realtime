from __future__ import annotations

from flask import Flask

from config import Config
from .extensions import db, socketio
from .models import Message, Room
from .routes import main_bp
from .services.chat_service import seed_default_rooms


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    socketio.init_app(app, async_mode='threading')
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        seed_default_rooms(app.config['DEFAULT_ROOMS'])

    from . import events  # noqa: F401

    return app
