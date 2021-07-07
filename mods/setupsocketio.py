from flask_socketio import join_room, rooms, ConnectionRefusedError
from mods.setupflask import socketio, client, usersinrooms, sessions, stdlibs
from mods.utilities import errorHandle
from mods.stdlib import mafstdlib
from flask import request
from time import time

@socketio.on('handshake')
def connection(json):
    if not client.mafiaredux.cookies.count_documents({'token': json['usertoken']}):
        raise ConnectionRefusedError('can\'t use a cookie to save their lives')
    room = json['roomId']
    join_room(room)
    userid = client.mafiaredux.cookies.find_one({'token': json['usertoken']}, {'token': 0, '_id': 0})['id']
    if room not in usersinrooms:
        usersinrooms[room] = []
    usersinrooms[room].append(request.sid)
    sessions[request.sid] = userid
    name = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    print(request.sid, 'resolved to', name, 'at', room)
    try:
        events = client.mafiaredux.rooms.find_one({'roomid': room}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})['events']
        print(events)
        for event in events:
            socketio.emit(*event, to=request.sid)
    except Exception as e:
        errorHandle(e)
    socketio.emit('userJoin', {
        'id': userid,
        'name': name,
        'timestamp': time()
    }, to=room)
    if room not in stdlibs:
        stdlibs[room] = mafstdlib(socketio, room)

@socketio.on('connect')
def connection():
    print(request.sid, 'has joined')

@socketio.on('disconnect')
def disconnect():
    room = rooms(request.sid)
    userid = sessions[request.sid]
    name = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    socketio.emit('userExit', {
        'id': userid,
        'name': name,
        'timestamp': time()
    }, to=room)
    usersinrooms[room[-1]].remove(request.sid)
    print(name, 'has left')

@socketio.on('chat')
def chat(message):
    room = rooms(request.sid)
    stdlib = stdlibs[room[-1]]
    print(sessions)
    userid = sessions[request.sid]
    name = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    print(name, 'says', repr(message))
    packet = {
        'timestamp': time(),
        'message': message,
        'from': name,
        'fromid': userid
    }
    socketio.emit('chat', packet, to=room)
    client.mafiaredux.rooms.update_one(
        {'roomid': room[-1]},
        {'$push': {'events': ['chat', packet]}}
    )
    print(room)