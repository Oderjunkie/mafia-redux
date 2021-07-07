from flask import request, render_template
from mods.setupflask import app

@app.route('/')
@app.route('/index.html')
def index():
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
def getgame(roomid: str):
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

@app.route('/ddroid.ttf')
def ddroidttf():
    return app.send_static_file('disposabledroidbb.ttf')

@app.route('/ddroid.woff')
def ddroidwoff():
    return app.send_static_file('disposabledroidbb.woff')

@app.route('/ddroid.woff2')
def ddroidwoff2():
    return app.send_static_file('disposabledroidbb.woff2')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# Favicon
##########

import mods.favicon