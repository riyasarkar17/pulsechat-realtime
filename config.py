from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URL', 'sqlite:///chat_app.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    APP_NAME: str = 'PulseChat'
    DEFAULT_ROOMS: tuple[str, ...] = ('general', 'developers', 'random')
    MAX_MESSAGE_LENGTH: int = 500
    MAX_USERNAME_LENGTH: int = 18
