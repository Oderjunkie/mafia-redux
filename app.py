from flask import Flask, request, jsonify
from flask_socketio import SocketIO
#from flask_pymongo import PyMongo
from random import choice
import pymongo
import os

app = Flask(__name__)
#app.config['MONGO_DBNAME'] = 'mafiaredux'
#app.config['MONGO_URI'] = os.environ['MONGODB']
socketio = SocketIO(app)
#client = pymongo.MongoClient(os.environ['MONGODB'])
client = pymongo.MongoClient(os.environ['MONGODB'])

#mongo = PyMongo(app)

# Index page + scripts
#######################

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/script.js')
def script():
    return app.send_static_file('script.js')

@app.route('/style.css')
def style():
    return app.send_static_file('style.css')

@app.route('/jquery-3.6.0.min.js')
def j360js():
    return app.send_static_file('jquery-3.6.0.min.js')

@app.route('/jquery-3.6.0.min.map')
def j360map():
    return app.send_static_file('jquery-3.6.0.min.map')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# Rooms requests
#################

##@app.route('/api/rooms')
##def rooms():
##    arr = []
##    for el in client.mafiaredux.rooms.find():
##        print(arr)
##        el.pop('_id')
##        arr.append(el)
##    return jsonify(arr)

def randChar(index):
    return choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-')

##@app.route('/api/makeroom', methods=['POST'])
##def makeroom():
##    name = request.form.get('name')
##    listed = request.form.get('listed')
##    roomid = ''.join(map(randChar, range(25)))
##    client.mafiaredux.rooms.insert_one({
##        'roomId': roomid,
##        'name': name,
##        'listed': listed
##    })

# Socket.io
############

# empty head wolololool


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
