from mods.utilities import randString, ReverseProxied
from flask_socketio import SocketIO
from mods.mscript import maflogic
from flask import Flask
import pymongo
import os

app = Flask('app')
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config['SECRET_KEY'] = randString(100)
socketio = SocketIO(app)
client = pymongo.MongoClient(os.environ['MONGODB'])

sessions: dict[str, str] = {}
usersinrooms: dict = {}
from mods.stdlib import mafstdlib
stdlibs: dict[str, mafstdlib] = {}
logics: dict[str, maflogic] = {}