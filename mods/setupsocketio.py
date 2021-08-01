from typing import Any
from mods.setupflask import socketio, client, usersinrooms, sessions, stdlibs, logics
from flask_socketio import join_room, rooms, ConnectionRefusedError
from mods.utilities import errorHandle, idname2key
from mods.mscript import maflogic
from mods.stdlib import mafstdlib
from mods.console import print
from urllib.parse import quote
from flask import request
from requests import get
from time import time

@socketio.on('handshake')
def connection(json):
    if not client.mafiaredux.cookies.count_documents({'token': json['usertoken']}):
        raise ConnectionRefusedError('can\'t use a cookie to save their lives')
    room: str = json['roomId']
    join_room(room)
    userid: str = client.mafiaredux.cookies.find_one({'token': json['usertoken']}, {'token': 0, '_id': 0})['id']
    if room not in usersinrooms:
        usersinrooms[room] = []
    usersinrooms[room].append(request.sid)
    sessions[request.sid] = userid
    name: str = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    print(request.sid, 'resolved to', name, 'at', room)
    roomobj = None
    try:
        roomobj: dict[str, Any] = client.mafiaredux.rooms.find_one({'roomid': room}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})
        events: list[list[Any]] = roomobj['events']
        #print(events)
        isHost: bool = roomobj['host']==userid
        socketio.emit('presence', {'player': False, 'host': isHost}, to=request.sid)
        socketio.emit('handshake', events, to=request.sid)
    #     for event in events:
    #         socketio.emit(*event, to=request.sid)
    except Exception as e:
        socketio.emit('error', 'Internal server error occured [getting events], Maybe you typed in an incorrect url?', to=room)
        # errorHandle(e)
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
            code: str = get('https://pastebin.com/raw/'+quote(roomobj['logic'], safe='')).content.decode('utf-8')
            logics[room].main(code)
            logics[room].funcs.setup(stdlibs[room])
        except Exception as e:
            socketio.emit('system', {
                'message': 'Game logic url was not valid, Logic is currently disabled.',
                'timestamp': time()
            }, to=room)
            raise e

@socketio.on('connect')
def connection():
    print(request.sid, 'has joined')

@socketio.on('disconnect')
def disconnect():
    room: list[str] = rooms(request.sid)
    userid: str = sessions[request.sid]
    name: str = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    socketio.emit('userExit', {
        'id': userid,
        'name': name,
        'timestamp': time()
    }, to=room)
    try:
        usersinrooms[room[-1]].remove(request.sid)
    except Exception as e:
        errorHandle(e)
    print(name, 'has left')

@socketio.on('logic')
def changeGameLogic(link):
    room: list[str] = rooms(request.sid)
    userid: str = sessions[request.sid]
    roomobj: dict = client.mafiaredux.rooms.find_one({'roomid': room[-1]}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})
    if userid == roomobj['host']:
        logics[room[-1]] = maflogic()
        logic: maflogic = logics[room[-1]]
        try:
            code = get('https://pastebin.com/raw/'+quote(roomobj['logic'], safe='')).content.decode('utf-8')
            logic.main(code)
            logic.funcs.setup(stdlibs[room])
        except Exception as e:
            socketio.emit('system', {
                'message': 'Game logic url was not valid, Logic is currently disabled.',
                'timestamp': time()
            }, to=room)
            raise e

@socketio.on('start')
def startGame():
    room: list[str] = rooms(request.sid)
    userid: str = sessions[request.sid]
    if userid == client.mafiaredux.rooms.find_one({'roomid': room[-1]}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0, 'logic': 0})['host']:
        stdlib: mafstdlib = stdlibs[room[-1]]
        logic: maflogic = logics[room[-1]]
        logic.funcs.start(stdlib)
        logic.funcs.distributeroles(stdlib)

@socketio.on('presence')
def presence(msg):
    room: list[str] = rooms(request.sid)
    stdlib: mafstdlib = stdlibs[room[-1]]
    userid: str = sessions[request.sid]
    name: str = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    if msg['host'] and userid != client.mafiaredux.rooms.find_one({'roomid': room[-1]}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0, 'logic': 0})['host']:
        socketio.emit('system', {
            'timestamp': time(),
            'message': '{} [ID:{}] is trying to hack mafia redux and gain host privileges, thankfully, they did not get it on the first try, eeeeeeeeediot.'.format(name, userid)
        }, to=room)
        return
    logic: maflogic = logics[room[-1]]
    if msg['player']:
        if logic.funcs.playerup(stdlib, userid, name) == False:
            return
    else:
        if logic.funcs.playerdown(stdlib, userid, name) == False:
            return
    socketio.emit('presence', msg, to=request.sid)

@socketio.on('gui')
def guichange(dicts: dict):
    room: list[str] = rooms(request.sid)
    stdlib: mafstdlib = stdlibs[room[-1]]
    userid: str = sessions[request.sid]
    logic: maflogic = logics[room[-1]]
    if logics[room[-1]].funcs.chat(stdlib, userid, dicts) in [None, True]:
        for name, value in dicts.items():
            logic.funcs.guichange(stdlib, userid, name, value)
            stdlib.guiselection[idname2key(userid, name)] = value

@socketio.on('chat')
def chat(message):
    room: list[str] = rooms(request.sid)
    userid: str = sessions[request.sid]
    stdlib: mafstdlib = stdlibs[room[-1]]
    print(sessions)
    name: str = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    if logics[room[-1]].funcs.chat(stdlib, userid, name, message) in [None, True]:
        print(name, 'says', repr(message))
        packet: dict = {
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