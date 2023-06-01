"""mecci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed

# def index(request):
#     global thread
#     if thread is None:
#         thread = sio.start_background_task(background_thread)
#     return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         sio.sleep(10)
#         count += 1
#         sio.emit('my_response', {'data': 'Server generated event'},
#                  namespace='/test')


# @sio.event
# def my_event(sid, message):
#     sio.emit('my_response', {'data': message['data']}, room=sid)
    
#     ...
    
#  @sio.event
# def disconnect(sid):
#     print('Client disconnected')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mutationapp.urls'))
]
