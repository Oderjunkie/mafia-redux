from mods.setupflask import socketio, client, usersinrooms, sessions, stdlibs, logics, print
from flask_socketio import join_room, rooms, ConnectionRefusedError
from mods.utilities import errorHandle
from mods.mscript import maflogic
from mods.stdlib import mafstdlib
from flask import request
from requests import get
from urllib.parse import quote
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
    roomobj = None
    try:
        roomobj = client.mafiaredux.rooms.find_one({'roomid': room}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})
        events = roomobj['events']
        print(events)
        isHost = roomobj['host']==userid
        socketio.emit('presence', {'player': False, 'host': isHost}, to=request.sid)
        socketio.emit('handshake', events, to=request.sid)
    #     for event in events:
    #         socketio.emit(*event, to=request.sid)
    except Exception as e:
        socketio.emit('error', 'Internal server error occured. [getting events]', to=room)
        errorHandle(e)
        return
    socketio.emit('userJoin', {
        'id': userid,
        'name': name,
        'timestamp': time()
    }, to=room)
    if room not in stdlibs:
        stdlibs[room] = mafstdlib(socketio, room)
    if room not in logics:
        logics[room] = maflogic()
        try:
            code = get('https://pastebin.com/raw/'+quote(roomobj['logic']))
        except Exception as e:
            socketio.emit('system', {
                'message': 'Game logic url was not valid, Logic is currently disabled.',
                'timestamp': time()
            }, to=room)
            errorHandle(e)
            return

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