from __future__ import annotations

from datetime import timezone
import re

from chat_app.extensions import db
from chat_app.models import Message, Room

ROOM_PATTERN = re.compile(r'^[a-z0-9-]{3,24}$')


def ensure_room(room_name: str) -> Room:
    room = Room.query.filter_by(name=room_name).first()
    if room is None:
        room = Room(name=room_name)
        db.session.add(room)
        db.session.commit()
    return room


def seed_default_rooms(default_rooms: tuple[str, ...] | list[str]) -> None:
    existing = {room.name for room in Room.query.all()}
    for room_name in default_rooms:
        if room_name not in existing:
            db.session.add(Room(name=room_name))
    db.session.commit()


def serialize_recent_messages(room_name: str, limit: int = 50) -> list[dict[str, str]]:
    room = Room.query.filter_by(name=room_name).first()
    if room is None:
        return []

    messages = (
        Message.query.filter_by(room_id=room.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    return [serialize_message(message) for message in reversed(messages)]


def create_message(username: str, room_name: str, body: str) -> dict[str, str]:
    room = ensure_room(room_name)

    message = Message(username=username, body=body, room_id=room.id)
    db.session.add(message)
    db.session.commit()
    return serialize_message(message)


def serialize_message(message: Message) -> dict[str, str]:
    local_time = message.created_at.astimezone(timezone.utc)
    return {
        'id': str(message.id),
        'username': message.username,
        'body': message.body,
        'room': message.room.name,
        'timestamp': local_time.strftime('%H:%M UTC'),
        'iso_timestamp': message.created_at.isoformat(),
    }


def normalize_username(username: str, max_length: int = 18) -> str:
    compact = re.sub(r'\s+', ' ', username).strip()
    if not compact:
        raise ValueError('Username cannot be empty.')
    if len(compact) > max_length:
        raise ValueError(f'Username must be {max_length} characters or fewer.')
    return compact


def normalize_message(body: str, max_length: int = 500) -> str:
    compact = re.sub(r'\s+', ' ', body).strip()
    if not compact:
        raise ValueError('Message cannot be empty.')
    if len(compact) > max_length:
        raise ValueError(f'Message must be {max_length} characters or fewer.')
    return compact


def validate_room_name(room_name: str) -> str:
    compact = room_name.strip().lower()
    if not ROOM_PATTERN.match(compact):
        raise ValueError('Room names must be 3-24 chars using lowercase letters, numbers, or hyphens.')
    return compact
