from django.urls import path
from applyapp import views

urlpatterns = [
    path('terraform-apply', views.terraformApply)
]
