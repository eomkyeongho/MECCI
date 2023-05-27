from django.urls import path
from mutationapp import views

urlpatterns = [
    path('iac-list', views.showIaCList),
    path('iac', views.showIaCDetail),
    path('random-iac', views.randomChoiceIaC),
    path('mutation', views.mutateIaC),
    path('validation', views.validateIaC),
    path('terraform-apply', views.terraformApply),
    path('upload-tf', views.uploadFile),
    path('injection', views.injectVulnerability),
]
