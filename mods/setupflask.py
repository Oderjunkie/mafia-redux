from utilities import randString, ReverseProxied
from flask_socketio import SocketIO
from flask import Flask
import pymongo
import os

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config['SECRET_KEY'] = randString(100)
socketio = SocketIO(app)
client = pymongo.MongoClient(os.environ['MONGODB'])
stdlibs = {}
logics = {}
sessions = {}
usersinrooms = {}