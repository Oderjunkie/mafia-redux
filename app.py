from flask import Flask, request, jsonify, render_template, redirect
from flask_socketio import SocketIO, join_room, leave_room, rooms
#from flask_pymongo import PyMongo
from binascii import hexlify
from random import choice
from time import time
import pymongo
import bcrypt
import os

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
#app.config['MONGO_DBNAME'] = 'mafiaredux'
#app.config['MONGO_URI'] = os.environ['MONGODB']
socketio = SocketIO(app)
#client = pymongo.MongoClient(os.environ['MONGODB'])
client = pymongo.MongoClient(os.environ['MONGODB'])
cookie2userid = {}

#mongo = PyMongo(app)

# Utilities
############

def randChar(index=None) -> str:
    return choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-')

def randString(length: int) -> str:
    return ''.join(map(randChar, range(length)))

# Index page + scripts
#######################

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/host.html')
def host():
    return app.send_static_file('host.html')

@app.route('/play.html')
def play():
    return app.send_static_file('play.html')

@app.route('/game/<string:roomid>')
def getgame(roomid=''):
    return app.send_static_file('specificgame.html')

@app.route('/script.js')
def script():
    return app.send_static_file('script.js')

@app.route('/play.js')
def playjs():
    return app.send_static_file('play.js')

@app.route('/host.js')
def hostjs():
    return app.send_static_file('host.js')

@app.route('/global.js')
def globaljs():
    return app.send_static_file('global.js')

@app.route('/specific.js')
def specjs():
    return app.send_static_file('specific.js')

@app.route('/style.css')
def style():
    return app.send_static_file('style.css')

@app.route('/host.css')
def hostcss():
    return app.send_static_file('host.css')

@app.route('/play.css')
def playcss():
    return app.send_static_file('play.css')

@app.route('/specific.css')
def speccss():
    return app.send_static_file('specific.css')

@app.route('/jquery-3.6.0.min.js')
def j360js():
    return app.send_static_file('jquery-3.6.0.min.js')

@app.route('/jquery-3.6.0.min.map')
def j360map():
    return app.send_static_file('jquery-3.6.0.min.map')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# Log in
#########

@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    userid = randString(30)
    userhash = bcrypt.hashpw(password.encode('latin-1'), bcrypt.gensalt())
    if client.mafiaredux.users.count_documents({'username': username}):
        return redirect('/usernametaken.html')
    client.mafiaredux.users.insert_one({
        'username': username,
        'userid': userid,
        'userhash': userhash
    })
    return redirect('/index.html')

@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = client.mafiaredux.users.find_one({'username': username}, {'username': 0, 'userid': 1, 'userhash': 1})
    if bcrypt.checkpw(password.encode('latin-1'), user['userhash']):
        return redirect('/index.html')
    return redirect('/badlogin.html')

# Rooms requests
#################

@app.route('/api/rooms')
def getrooms():
    arr = []
    for el in client.mafiaredux.rooms.find({}):
        print(arr)
        el.pop('_id')
        arr.append(el)
    return jsonify(arr)

@app.route('/api/makeroom', methods=['POST'])
def makeroom():
    name = request.form.get('name')
    listed = request.form.get('listed')
    print(name, listed)
    roomid = randString(25)
    client.mafiaredux.rooms.insert_one({
        'roomId': roomid,
        'name': name,
        'listed': listed=='on'
    })
    return redirect('/game/'+roomid)

def encode(string: str) -> str:
    return ''.join(['\\x'+hexlify(bytes([char])).decode('latin1') for char in string.encode('latin1')])

# Socket.io
############

sessions = {}

@socketio.on('handshake')
def connection(json):
    join_room(json['roomId'])
    userid = request.sid #json['userId']
    socketio.emit('userJoin', {'id': userid})
    sessions[request.sid] = userid
    print(request.sid, 'resolved to', userid)

@socketio.on('connect')
def connection():
    print(request.sid, 'has joined')

@socketio.on('disconnect')
def disconnect():
    print(sessions[request.sid], 'has left')

@socketio.on('chat')
def chat(message):
    print(sessions[request.sid], 'says', repr(message))
    room = rooms(request.sid)
    socketio.emit('chat', {
        'timestamp': time(),
        'message': message,
        'from': str(sessions[request.sid])},
    to=room)

# Favicon
##########

@app.route('/android-chrome-192x192.png')
def a192():
    return app.send_static_file('android-chrome-192x192.png')

@app.route('/android-chrome-512x512.png')
def a512():
    return app.send_static_file('android-chrome-512x512.png')

@app.route('/favicon-16x16.png')
def f16():
    return app.send_static_file('favicon-chrome-16x16.png')

@app.route('/favicon-32x32.png')
def f32():
    return app.send_static_file('favicon-32x32.png')

@app.route('/favicon.ico')
def fico():
    return app.send_static_file('favicon.ico')

@app.route('/site.webmanifest')
def manif():
    return app.send_static_file('site.webmanifest')

# Init code
############

if __name__ == '__main__':
    socketio.run(app)
    #app.run()
