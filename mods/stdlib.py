from mods.setupflask import client, sessions, usersinrooms
from mods.utilities import addto
from time import time

class mafstdlib:
    def __init__(self, socket, room):
        self.socket = socket
        self.room = room
        self.vars = {}
    def system(self, msg):
        self.socket.emit('system', {
            'timestamp': time(),
            'message': msg
        }, to=self.room)
    def systemto(self, useridto, msg):
        sid = list(sessions.values())[list(sessions.keys()).index(useridto)]
        self.socket.emit('system', {
            'timestamp': time(),
            'message': msg
        }, to=sid)
    def sendas(self, useridas, username, msg):
        self.socket.emit('chat', {
            'timestamp': time(),
            'message': msg,
            'from': username,
            'fromid': useridas
        }, to=self.room)
    def sendasto(self, useridas, username, useridto, msg):
        sid = list(sessions.values())[list(sessions.keys()).index(useridto)]
        self.socket.emit('chat', {
            'timestamp': time(),
            'message': msg,
            'from': username,
            'fromid': useridas
        }, to=sid)
    def kill(self, userid):
        name = client.mafiaredux.users.find_one({'userid': userid}, {'userid': 0, 'userhash': 0, '_id': 0})['username']
        self.socket.emit('kill', {
            'timestamp': time(),
            'id': userid,
            'name': name
        }, to=self.room)
    def makearr(self, *els):
        return els
    def makedict(self, *kvs):
        return dict(zip(kvs[::2], kvs[1::2]))
    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b
    def mul(self, a, b):
        return a * b
    def div(self, a, b):
        return a / b
    from math import floor
    from math import ceil
    from builtins import len
    from builtins import int
    def find(self, arr, val):
        return arr.index(val)
    def count(self, arr, val):
        return arr.count(val)
    from builtins import max
    from builtins import min
    def eq(self, a, b):
        return a==b
    def neq(self, a, b):
        return a!=b
    def gt(self, a, b):
        return a>b
    def lt(self, a, b):
        return a<b
    def gte(self, a, b):
        return a>=b
    def lte(self, a, b):
        return a<=b
    def set(self, var, val):
        self.vars[var] = val
    def get(self, var, val):
        return self.vars[var]
    def getallusers(self):
        return map(sessions.get, usersinrooms[self.room])
    def getallusernames(self): # TODO: stop lazying
        pass #    return map(sessions.get, usersinrooms[self.room])
    def getname(self, instance):
        return type(instance).__name__
    def getprop(self, instance, prop):
        return instance.prop
    def getindex(self, obj, index):
        return obj[index]
    def setprop(self, instance, prop, val):
        instance.prop = val
        return val
    def setindex(self, obj, index, val):
        obj[index] = val
        return val
    def format(self, string, *args):
        return string.format(*args)
    def makegui(self, role, name, names, values):
        pass
    def getgui(self, role, name):
        pass
    def getguiname(self, role, name):
        pass
    def freezegui(self, role, name):
        pass
    def apply(self, func, *args):
        return func(*args)
    from random import randint as rand
@addto(mafstdlib, 'and')
def _(self, a, b):
    return a and b
@addto(mafstdlib, 'or')
def _(self, a, b):
    return a or b
@addto(mafstdlib, 'not')
def _(self, a):
    return not a
@addto(mafstdlib, 'return')
def _(self, val):
    return val