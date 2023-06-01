"""
WSGI config for mecci project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
import eventlet
import eventlet.wsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecci.settings')

application = get_wsgi_application()
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*', cors_credentials=True)
application = socketio.WSGIApp(sio, application)


# @sio.event
# def TEST(sid, message):
#     print(message['data'])
#     sio.emit('my_response', {'data': message['data']})

# @sio.event
# def disconnect_request(sid):
#     sio.disconnect(sid)

# @sio.event
# def connect(sid, environ):
#     sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


# @sio.event
# def disconnect(sid):
#     print('Client disconnected')


# if __name__ == '__main__':
#     if sio.async_mode == 'threading':
#         # deploy with Werkzeug
#         app.run(threaded=True)
#     elif sio.async_mode == 'eventlet':
#         # deploy with eventlet
#         import eventlet
#         import eventlet.wsgi
#         eventlet.wsgi.server(eventlet.listen(('', 8083)), app)
#     elif sio.async_mode == 'gevent':
#         # deploy with gevent
#         from gevent import pywsgi
#         try:
#             from geventwebsocket.handler import WebSocketHandler
#             websocket = True
#         except ImportError:
#             websocket = False
#         if websocket:
#             pywsgi.WSGIServer(('', 8083), app,
#                               handler_class=WebSocketHandler).serve_forever()
#         else:
#             pywsgi.WSGIServer(('', 8083), app).serve_forever()
#     elif sio.async_mode == 'gevent_uwsgi':
#         print('Start the application through the uwsgi server. Example:')
#         print('uwsgi --http :8083 --gevent 1000 --http-websockets --master '
#               '--wsgi-file app.py --callable app')
#     else:
#         print('Unknown async_mode: ' + sio.async_mode)