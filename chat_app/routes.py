from __future__ import annotations

from flask import Blueprint, current_app, render_template

from .models import Room


main_bp = Blueprint('main', __name__)


@main_bp.get('/')
def index():
    rooms = Room.query.order_by(Room.name.asc()).all()
    room_names = [room.name for room in rooms] or list(current_app.config['DEFAULT_ROOMS'])
    return render_template(
        'index.html',
        app_name=current_app.config['APP_NAME'],
        rooms=room_names,
        max_message_length=current_app.config['MAX_MESSAGE_LENGTH'],
        max_username_length=current_app.config['MAX_USERNAME_LENGTH'],
    )
