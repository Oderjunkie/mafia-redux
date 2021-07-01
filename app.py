from flask import Flask, request, jsonify, render_template, redirect, make_response, session
from flask_socketio import SocketIO, join_room, leave_room, rooms, ConnectionRefusedError
#from flask_pymongo import PyMongo
from binascii import hexlify
from random import choice
from time import time
import pymongo
import bcrypt
import os

# Utilities
############

def errorHandle(e):
    line = e.__traceback__.tb_lineno-1
    print('File "{}", line {}, in {}'.format(e.__traceback__.tb_frame.f_code.co_filename,
                                         line,
                                         e.__traceback__.tb_frame.f_code.co_name))
    with open(e.__traceback__.tb_frame.f_code.co_filename) as f:
        lines = f.readlines()
        print('    {}\t{}'.format(line-1, lines[line-1][:-1]))
        print('>>> {}\t{}'.format(line,   lines[line][:-1]))
        print('    {}\t{}'.format(line+1, lines[line+1][:-1]))
        print('{}: {}'.format(str(type(e))[8:-2], str(e)))
        f.close()

def randChar(index=None) -> str:
    return choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-')

def randString(length: int) -> str:
    return ''.join(map(randChar, range(length)))

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
app.config['SECRET_KEY'] = randString(100)
#app.config['MONGO_DBNAME'] = 'mafiaredux'
#app.config['MONGO_URI'] = os.environ['MONGODB']
socketio = SocketIO(app)
#client = pymongo.MongoClient(os.environ['MONGODB'])
client = pymongo.MongoClient(os.environ['MONGODB'])
cookie2userid = {}

#mongo = PyMongo(app)

# Index page + scripts
#######################

@app.route('/')
def index():
    return app.send_static_file('under_renovation.html')

@app.route('/index.html')
def index2():
    return app.send_static_file('index.html')

@app.route('/login.html')
def login():
    return app.send_static_file('login.html')

@app.route('/host.html')
def host():
    return app.send_static_file('host.html')

@app.route('/play.html')
def play():
    return app.send_static_file('play.html')

@app.route('/game/<string:roomid>')
def getgame(roomid=''):
    print(request.cookies.get('usertoken'))
    return render_template('specificgame.html')

@app.route('/script.js')
def script():
    return app.send_static_file('script.js')

@app.route('/play.js')
def playjs():
    return app.send_static_file('play.js')

@app.route('/host.js')
def hostjs():
    return app.send_static_file('host.js')

@app.route('/login.js')
def loginjs():
    return app.send_static_file('login.js')

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
def registerapi():
    username = request.form.get('username')
    if client.mafiaredux.users.count_documents({'username': username}):
        return 'That username is taken.', 422
    password = request.form.get('password')
    userid = randString(30)
    userhash = bcrypt.hashpw(password.encode('latin-1'), bcrypt.gensalt())
    #print(userhash)
    client.mafiaredux.users.insert_one({
        'username': username,
        'userid': userid,
        'userhash': userhash
    })
    usertoken = randString(30)
    cookie2userid[usertoken] = userid
    resp = make_response('/index.html', 200)
    resp.set_cookie('usertoken', value=usertoken)
    return resp

@app.route('/api/login', methods=['POST'])
def loginapi():
    username = request.form.get('username')
    password = request.form.get('password')
    #print('LOGIN', username, password)
    try:
        user = client.mafiaredux.users.find_one({'username': username}, {'username': 0, '_id': 0})
        if user:
            if bcrypt.checkpw(password.encode('latin-1'), user['userhash']):
                usertoken = randString(30)
                cookie2userid[usertoken] = user['userid']
                resp = make_response('/index.html', 200)
                resp.set_cookie('usertoken', value=usertoken)
                return resp
            return 'Bad password.', 401
    except Exception as e:
        print(type(e), e)
    return 'No such user found.', 404

# Rooms requests
#################

@app.route('/api/rooms')
def getroomsapi():
    arr = []
    return jsonify(list(client.mafiaredux.rooms.find({'listed': True}, {'_id': 0, 'events': 0, 'listed': 0})))

@app.route('/api/makeroom', methods=['POST'])
def makeroomapi():
    name = request.form.get('name')
    listed = request.form.get('listed')
    print(name, listed)
    roomid = randString(25)
    client.mafiaredux.rooms.insert_one({
        'roomid': roomid,
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
    if json['usertoken'] not in cookie2userid:
        raise ConnectionRefusedError('can\'t use a cookie to save their lives')
    room = json['roomId']
    join_room(room)
    userid = cookie2userid[json['usertoken']]
    socketio.emit('userJoin', {'id': userid}, to=room)
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

@socketio.on('connect')
def connection():
    print(request.sid, 'has joined')

@socketio.on('disconnect')
def disconnect():
    name = client.mafiaredux.users.find_one({'userid': sessions[request.sid]}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    print(name, 'has left')

@socketio.on('chat')
def chat(message):
    room = rooms(request.sid)
    print(sessions)
    name = client.mafiaredux.users.find_one({'userid': sessions[request.sid]}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
    print(name, 'says', repr(message))
    packet = {
        'timestamp': time(),
        'message': message,
        'from': name
    }
    socketio.emit('chat', packet, to=room)
    print(room)
    #oldevents = client.mafiaredux.rooms.find_one({'roomid': room[-1]}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})['events']
    client.mafiaredux.rooms.update_one(
        {'roomid': room[-1]},
        {'$push': {'events': ['chat', packet]}}
    )
    #newevents = client.mafiaredux.rooms.find_one({'roomid': room[-1]}, {'_id': 0, 'setup': 0, 'listed': 0, 'roomid': 0, 'name': 0})['events']
    #print(oldevents, newevents)

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
