from mods.setupflask import app

@app.route('/android-chrome-192x192.png')
def a192():
    return app.send_static_file('favicon/android-chrome-192x192.png')

@app.route('/android-chrome-512x512.png')
def a512():
    return app.send_static_file('favicon/android-chrome-512x512.png')

@app.route('/favicon-16x16.png')
def f16():
    return app.send_static_file('favicon/favicon-chrome-16x16.png')

@app.route('/favicon-32x32.png')
def f32():
    return app.send_static_file('favicon/favicon-32x32.png')

@app.route('/favicon.ico')
def fico():
    return app.send_static_file('favicon/favicon.ico')

@app.route('/site.webmanifest')
def manif():
    return app.send_static_file('favicon/site.webmanifest')
