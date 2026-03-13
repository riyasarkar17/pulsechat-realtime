# PulseChat

A sleek real-time multi-room chat application built with **Python, Flask, Socket.IO, and SQLite**.

![PulseChat Preview](https://img.shields.io/badge/Status-Ready%20to%20Run-22c55e?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-RealTime-010101?style=for-the-badge&logo=socketdotio&logoColor=white)

## Overview

PulseChat is designed as a polished portfolio project for a Python-focused GitHub profile. It includes:

- Real-time messaging with WebSockets
- Multiple chat rooms
- Persistent message history with SQLite
- Live online-user panel
- Responsive glassmorphism UI
- Clean folder structure for GitHub presentation
- Docker support and environment example
- Basic tests with `pytest`

## Tech Stack

- **Backend:** Flask, Flask-SocketIO, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Database:** SQLite
- **Testing:** pytest
- **Containerization:** Docker, docker-compose

## Project Structure

```text
pulsechat-realtime/
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── scripts/
│   └── run.sh
├── chat_app/
│   ├── __init__.py
│   ├── events.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   └── chat_service.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── chat.js
│   └── templates/
│       ├── base.html
│       └── index.html
└── tests/
    └── test_chat_service.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd pulsechat-realtime
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

```bash
python app.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Run with Docker

```bash
docker compose up --build
```

Then visit:

```text
http://127.0.0.1:5000
```

## Run Tests

```bash
pytest
```

## Features Walkthrough

### Join Flow
- Pick a display name
- Select a room
- Start chatting instantly

### Chat Experience
- Messages appear live without refresh
- Active room members update automatically
- Message history remains available after reloads
- You can create extra rooms from the sidebar

## Future Improvements

- Direct messages
- Typing indicators between users
- Auth system with login/signup
- Emoji picker
- Message deletion/editing
- Dark/light theme toggle
- Cloud deployment

## License

MIT
