from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import gpt

# Create your views here.
def index(request):
    data = {}
    data["origin"], data["mutation"] = gpt.mutationIaC()
    return JsonResponse(data)
