print(f'{__name__}.py Loaded')

from mods.utilities import randString, ReverseProxied
from flask_socketio import SocketIO
from flask import Flask
import pymongo
import os

app = Flask('app')
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config['SECRET_KEY'] = randString(100)
socketio = SocketIO(app)
client = pymongo.MongoClient(os.environ['MONGODB'])
stdlibs = {}
logics = {}
sessions = {}
usersinrooms = {}