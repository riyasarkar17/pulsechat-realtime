from __future__ import annotations

from collections import defaultdict

from flask import current_app, request
from flask_socketio import emit, join_room, leave_room

from .extensions import socketio
from .services.chat_service import (
    create_message,
    ensure_room,
    normalize_message,
    normalize_username,
    serialize_recent_messages,
    validate_room_name,
)

active_sessions: dict[str, dict[str, str]] = {}
room_users: dict[str, set[str]] = defaultdict(set)


def emit_room_state(room_name: str) -> None:
    users = sorted(room_users.get(room_name, set()), key=str.lower)
    emit(
        'room_state',
        {
            'room': room_name,
            'users': users,
            'count': len(users),
        },
        to=room_name,
    )


@socketio.on('connect')
def handle_connect():
    emit('connected', {'message': 'Connected to PulseChat.'})


@socketio.on('join_room')
def handle_join_room(payload: dict):
    try:
        username = normalize_username(
            payload.get('username', ''),
            current_app.config['MAX_USERNAME_LENGTH'],
        )
        room_name = validate_room_name(payload.get('room', 'general'))
    except ValueError as exc:
        emit('error_message', {'message': str(exc)}, to=request.sid)
        return
    sid = request.sid

    previous_session = active_sessions.get(sid)
    if previous_session:
        old_room = previous_session['room']
        leave_room(old_room)
        room_users[old_room].discard(previous_session['username'])
        emit(
            'system_message',
            {
                'body': f"{previous_session['username']} left the room.",
                'timestamp': 'now',
            },
            to=old_room,
        )
        emit_room_state(old_room)

    ensure_room(room_name)
    join_room(room_name)
    active_sessions[sid] = {'username': username, 'room': room_name}
    room_users[room_name].add(username)

    emit(
        'room_history',
        {
            'room': room_name,
            'messages': serialize_recent_messages(room_name),
        },
        to=sid,
    )
    emit(
        'system_message',
        {
            'body': f'{username} joined #{room_name}.',
            'timestamp': 'now',
        },
        to=room_name,
    )
    emit_room_state(room_name)


@socketio.on('send_message')
def handle_send_message(payload: dict):
    sid = request.sid
    session = active_sessions.get(sid)
    if not session:
        emit('error_message', {'message': 'Join a room before sending messages.'}, to=sid)
        return

    try:
        body = normalize_message(
            payload.get('body', ''),
            current_app.config['MAX_MESSAGE_LENGTH'],
        )
    except ValueError as exc:
        emit('error_message', {'message': str(exc)}, to=sid)
        return

    message = create_message(session['username'], session['room'], body)
    emit('new_message', message, to=session['room'])


@socketio.on('disconnect')
def handle_disconnect():
    session = active_sessions.pop(request.sid, None)
    if not session:
        return

    room_name = session['room']
    username = session['username']
    room_users[room_name].discard(username)
    leave_room(room_name)
    emit(
        'system_message',
        {
            'body': f'{username} disconnected.',
            'timestamp': 'now',
        },
        to=room_name,
    )
    emit_room_state(room_name)
