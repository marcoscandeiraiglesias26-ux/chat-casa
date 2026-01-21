import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreto_aula_123'
socketio = SocketIO(app, cors_allowed_origins="*")

# Diccionario para rastrear cuánta gente hay
users_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global users_count
    users_count += 1
    emit('update_users', users_count, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global users_count
    users_count -= 1
    emit('update_users', users_count, broadcast=True)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    # Avisar a la sala que alguien entró
    emit('status', {'msg': f"{data['user']} ha entrado a la sala."}, room=room)

@socketio.on('message')
def handle_message(data):
    # Solo envía el mensaje a la sala específica
    emit('message', data, room=data['room'])

@socketio.on('typing')
def handle_typing(data):
    emit('display_typing', data, room=data['room'], include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
