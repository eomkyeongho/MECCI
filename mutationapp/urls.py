from django.urls import path
from mutationapp import views

urlpatterns = [
    path('mutate', views.mutateCode),
    path('origin', views.getOrigin),
    path('validate', views.validate),
    path('iac-list', views.showIaCList),
]
