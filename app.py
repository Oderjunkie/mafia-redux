from mods.setupflask import socketio, app # Flask and friends
import mods.stdlib # I/O
import mods.routes # Index page + scripts + favicon
import mods.api # API
import mods.setupsocketio # Socket.io

# Init code
############

if __name__ == '__main__':
    socketio.run(app)
