from flask import request, render_template
from mods.setupflask import app

def send_sass(name: str):
    res = app.send_static_file('sass/'+name)
    res.mimetype = 'text/css'
    return res

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/host.html')
def host():
    return render_template('host.html')

@app.route('/play.html')
def play():
    return render_template('play.html')

@app.route('/game/<string:roomid>')
def getgame(roomid: str):
    print(request.cookies.get('usertoken'))
    return render_template('specificgame.html')

@app.route('/renovation.js')
def renovationjs():
    return app.send_static_file('javascript/renovation.js')

@app.route('/script.js')
def script():
    return app.send_static_file('javascript/script.js')

@app.route('/play.js')
def playjs():
    return app.send_static_file('javascript/play.js')

@app.route('/host.js')
def hostjs():
    return app.send_static_file('javascript/host.js')

@app.route('/login.js')
def loginjs():
    return app.send_static_file('javascript/login.js')

@app.route('/global.js')
def globaljs():
    return app.send_static_file('javascript/global.js')

@app.route('/renovation.css')
def renovationcss():
    return send_sass('renovation.scss')

@app.route('/style.css')
def style():
    return send_sass('style.scss')

@app.route('/host.css')
def hostcss():
    return send_sass('host.scss')

@app.route('/play.css')
def playcss():
    return send_sass('play.scss')

@app.route('/specific.css')
def speccss():
    return send_sass('specific.scss')

@app.route('/jquery-3.6.0.min.js')
def j360js():
    return app.send_static_file('libs/jquery-3.6.0.min.js')

@app.route('/jquery-3.6.0.min.map')
def j360map():
    return app.send_static_file('libs/jquery-3.6.0.min.map')

@app.route('/ddroid.ttf')
def ddroidttf():
    return app.send_static_file('font/disposabledroidbb.ttf')

@app.route('/ddroid.woff')
def ddroidwoff():
    return app.send_static_file('font/disposabledroidbb.woff')

@app.route('/ddroid.woff2')
def ddroidwoff2():
    return app.send_static_file('font/disposabledroidbb.woff2')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# Favicon
##########

import mods.favicon