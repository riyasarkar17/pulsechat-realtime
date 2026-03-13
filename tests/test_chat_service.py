from __future__ import annotations

import pytest

from chat_app import create_app
from chat_app.extensions import db
from chat_app.models import Room
from chat_app.services.chat_service import (
    normalize_message,
    normalize_username,
    seed_default_rooms,
    validate_room_name,
)


class TestConfig:
    TESTING = True
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_NAME = 'PulseChat'
    DEFAULT_ROOMS = ('general', 'developers', 'random')
    MAX_MESSAGE_LENGTH = 500
    MAX_USERNAME_LENGTH = 18


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


def test_seed_default_rooms_is_idempotent(app):
    with app.app_context():
        seed_default_rooms(('general', 'general', 'random'))
        rooms = [room.name for room in Room.query.order_by(Room.name.asc()).all()]
        assert rooms == ['developers', 'general', 'random']


def test_normalize_username_compacts_whitespace():
    assert normalize_username('  Riya   Sarkar  ') == 'Riya Sarkar'


def test_normalize_message_rejects_empty_value():
    with pytest.raises(ValueError):
        normalize_message('   ')


def test_validate_room_name_accepts_slug_format():
    assert validate_room_name('  design-lab ') == 'design-lab'


def test_validate_room_name_rejects_invalid_name():
    with pytest.raises(ValueError):
        validate_room_name('Bad Room!')
