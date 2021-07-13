from flask import request, make_response, jsonify, redirect
from mods.utilities import randString, errorHandle
from mods.setupflask import app, client, print
import bcrypt

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
    client.mafiaredux.users.insert_one({
        'username': username,
        'userid': userid,
        'userhash': userhash
    })
    usertoken = randString(30)
    client.mafiaredux.cookies.insert_one({
        'token': usertoken,
        'id': userid
    })
    resp = make_response('/index.html', 200)
    resp.set_cookie('usertoken', value=usertoken)
    return resp

@app.route('/api/login', methods=['POST'])
def loginapi():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        user = client.mafiaredux.users.find_one({'username': username}, {'username': 0, '_id': 0})
        if user:
            if bcrypt.checkpw(password.encode('latin-1'), user['userhash']):
                usertoken = randString(30)
                client.mafiaredux.cookies.insert_one({
                    'token': usertoken,
                    'id': user['userid']
                })
                resp = make_response('/index.html', 200)
                resp.set_cookie('usertoken', value=usertoken)
                return resp
            return 'Bad password.', 401
    except Exception as e:
        errorHandle(e)
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