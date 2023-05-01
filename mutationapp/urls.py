from django.urls import path
from mutationapp import views

urlpatterns = [
    path('', views.index),
]
