print(f'{__name__}.py Loaded')
print(f'BEFORE {__name__} URL_MAP: {app.url_map}')

from mods.setupflask import socketio, app # Flask and friends
import mods.stdlib # I/O
import mods.routes # Index page + scripts + favicon
import mods.api # API
import mods.setupsocketio # Socket.io

print(f'AFTER {__name__} URL_MAP: {app.url_map}')

# Init code
############

if __name__ == '__main__':
    socketio.run(app)
