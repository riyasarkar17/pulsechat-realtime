const socket = io();

const joinModal = document.getElementById('join-modal');
const joinForm = document.getElementById('join-form');
const joinError = document.getElementById('join-error');
const usernameInput = document.getElementById('username-input');
const roomSelect = document.getElementById('room-select');
const roomList = document.getElementById('room-list');
const activeRoomLabel = document.getElementById('active-room-label');
const userList = document.getElementById('user-list');
const onlineCount = document.getElementById('online-count');
const messageBoard = document.getElementById('message-board');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const typingState = document.getElementById('typing-state');
const newRoomButton = document.getElementById('new-room-button');

const state = {
  username: localStorage.getItem('pulsechat.username') || '',
  room: localStorage.getItem('pulsechat.room') || window.APP_CONFIG.rooms[0] || 'general',
  rooms: [...window.APP_CONFIG.rooms],
};

function escapeRoom(room) {
  return room.trim().toLowerCase();
}

function renderRoomOptions() {
  roomSelect.innerHTML = '';
  roomList.innerHTML = '';

  state.rooms.forEach((room) => {
    const option = document.createElement('option');
    option.value = room;
    option.textContent = `#${room}`;
    option.selected = room === state.room;
    roomSelect.appendChild(option);

    const button = document.createElement('button');
    button.type = 'button';
    button.className = `room-chip ${room === state.room ? 'active' : ''}`;
    button.dataset.room = room;
    button.innerHTML = `<span>#${room}</span><span>→</span>`;
    button.addEventListener('click', () => joinSelectedRoom(room));
    roomList.appendChild(button);
  });
}

function addSystemBanner(text) {
  const banner = document.createElement('div');
  banner.className = 'system-banner';
  banner.textContent = text;
  messageBoard.appendChild(banner);
  scrollToBottom();
}

function renderMessage(message) {
  const row = document.createElement('article');
  row.className = `message-row ${message.username === state.username ? 'self' : ''}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  const meta = document.createElement('div');
  meta.className = 'message-meta';

  const author = document.createElement('span');
  author.className = 'message-author';
  author.textContent = message.username;

  const time = document.createElement('span');
  time.className = 'message-time';
  time.textContent = message.timestamp;

  const text = document.createElement('div');
  text.className = 'message-text';
  text.textContent = message.body;

  meta.append(author, time);
  bubble.append(meta, text);
  row.appendChild(bubble);
  messageBoard.appendChild(row);
  scrollToBottom();
}

function renderHistory(messages) {
  messageBoard.innerHTML = '';
  if (!messages.length) {
    const empty = document.createElement('div');
    empty.className = 'empty-state';
    empty.textContent = 'No messages yet. Start the conversation.';
    messageBoard.appendChild(empty);
    return;
  }

  messages.forEach(renderMessage);
}

function renderUsers(users) {
  userList.innerHTML = '';
  onlineCount.textContent = String(users.length);

  if (!users.length) {
    const li = document.createElement('li');
    li.className = 'user-chip';
    li.textContent = 'No one online';
    userList.appendChild(li);
    return;
  }

  users.forEach((user) => {
    const li = document.createElement('li');
    li.className = 'user-chip';
    li.textContent = user;
    userList.appendChild(li);
  });
}

function scrollToBottom() {
  messageBoard.scrollTop = messageBoard.scrollHeight;
}

function joinSelectedRoom(room) {
  if (!state.username) {
    state.room = room;
    renderRoomOptions();
    return;
  }

  state.room = room;
  localStorage.setItem('pulsechat.room', room);
  renderRoomOptions();
  activeRoomLabel.textContent = `#${room}`;
  typingState.textContent = `Switched to #${room}.`;
  socket.emit('join_room', { username: state.username, room });
}

joinForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const username = usernameInput.value.trim();
  const room = roomSelect.value;

  if (!username) {
    joinError.textContent = 'Please enter a display name.';
    return;
  }

  if (username.length > window.APP_CONFIG.maxUsernameLength) {
    joinError.textContent = `Use ${window.APP_CONFIG.maxUsernameLength} characters or fewer.`;
    return;
  }

  joinError.textContent = '';
  state.username = username;
  state.room = room;
  localStorage.setItem('pulsechat.username', username);
  localStorage.setItem('pulsechat.room', room);
  joinModal.style.display = 'none';
  activeRoomLabel.textContent = `#${room}`;
  socket.emit('join_room', { username, room });
});

messageForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const body = messageInput.value.trim();
  if (!body) {
    return;
  }

  if (body.length > window.APP_CONFIG.maxMessageLength) {
    typingState.textContent = `Messages are limited to ${window.APP_CONFIG.maxMessageLength} characters.`;
    return;
  }

  socket.emit('send_message', { body });
  messageInput.value = '';
  typingState.textContent = 'Delivered.';
});

messageInput.addEventListener('input', () => {
  typingState.textContent = messageInput.value ? 'Composing a message...' : 'Ready to chat.';
});

newRoomButton.addEventListener('click', () => {
  const room = window.prompt('Enter a new room name (lowercase letters, numbers, hyphens):');
  if (!room) {
    return;
  }

  const normalized = escapeRoom(room);
  const valid = /^[a-z0-9-]{3,24}$/.test(normalized);
  if (!valid) {
    typingState.textContent = 'Room names must be 3-24 chars using lowercase letters, numbers, or hyphens.';
    return;
  }

  if (!state.rooms.includes(normalized)) {
    state.rooms.push(normalized);
  }
  renderRoomOptions();
  joinSelectedRoom(normalized);
});

socket.on('connected', () => {
  usernameInput.value = state.username;
  renderRoomOptions();
  roomSelect.value = state.room;

  if (state.username) {
    joinModal.style.display = 'none';
    activeRoomLabel.textContent = `#${state.room}`;
    socket.emit('join_room', { username: state.username, room: state.room });
  } else {
    joinModal.style.display = 'grid';
  }
});

socket.on('room_history', (payload) => {
  state.room = payload.room;
  localStorage.setItem('pulsechat.room', state.room);
  activeRoomLabel.textContent = `#${payload.room}`;
  renderRoomOptions();
  renderHistory(payload.messages || []);
  typingState.textContent = `You are chatting in #${payload.room}.`;
});

socket.on('new_message', (payload) => {
  const emptyState = messageBoard.querySelector('.empty-state');
  if (emptyState) {
    emptyState.remove();
  }
  renderMessage(payload);
});

socket.on('system_message', (payload) => {
  addSystemBanner(payload.body);
});

socket.on('room_state', (payload) => {
  if (payload.room === state.room) {
    renderUsers(payload.users || []);
  }
});

socket.on('error_message', (payload) => {
  typingState.textContent = payload.message;
});
