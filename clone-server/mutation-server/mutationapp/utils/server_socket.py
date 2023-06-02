# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed

from flask import Flask, render_template
from flask_cors import CORS, cross_origin
import socketio

async_mode = None

sio = socketio.Server(logger=True, async_mode=async_mode,cors_allowed_origins="*")
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
# app.config['SECRET_KEY'] = 'secret!'
# app.config["CORS_HEADERS"]='Content-Type'
thread = None

@sio.event
def sendMessage(sid, message):
    #print(message['data'])
    sio.emit('my_response', {'data': message['data']})

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


# @sio.event
# def connect(sid, environ):
#     sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
#     sio.setSoTimeout(100);


@sio.event
def disconnect(sid):
    print('Client disconnected')
    sio.disconnect(sid)

if __name__ == '__main__':
    if sio.async_mode == 'threading':
        # deploy with Werkzeug
        app.run(threaded=True)
    elif sio.async_mode == 'eventlet':
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 8086)), app)
    elif sio.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 8086), app,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 8086), app).serve_forever()
    elif sio.async_mode == 'gevent_uwsgi':
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :8086 --gevent 1000 --http-websockets --master '
              '--wsgi-file app.py --callable app')
    else:
        print('Unknown async_mode: ' + sio.async_mode)