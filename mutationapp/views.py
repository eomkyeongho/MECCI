from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import gpt
import os
import time
import random
import requests

# Create your views here.
def showIaCList(request):
    data = {}

    fileList = [f.replace('.tf', '') for f in os.listdir("mutationapp/iac") if ".tf" in f]
    
    data["fileList"] = fileList
    
    return JsonResponse(data)

def showIaCDetail(request):
    data = {}

    fileName = request.GET.get('fileName')

    try:
        iac = open(f'mutationapp/iac/{fileName}.tf', 'r')
        data["iac"] = iac.read()
        iac.close()
    except:
        data["iac"] = 'not exist'

    return JsonResponse(data) 

def randomChoiceIaC(request):
    data ={}

    fileList = [f for f in os.listdir("mutationapp/iac") if ".tf" in f]
    fileName = random.choice(fileList)

    data["fileName"] = fileName.replace('.tf', '')

    iac = open(f'mutationapp/iac/{fileName}', 'r')
    data["iac"] = iac.read()
    iac.close()

    return JsonResponse(data)

def mutateIaC(request):
    data = {}

    fileName = request.GET.get('fileName')

    data["mutated"], data["diff"] = gpt.mutateIaC(fileName)
    
    return JsonResponse(data)

def terraformApply(request):
    data = {}

    try:
        f = open('main.tf', 'r')
        maintf = f.read()
        f.close()
        response = requests.post("http://121.135.134.175:8000/terraform-apply", data={'iac' : maintf})
        data["result"] = 'success'
    except:
        data["result"] = 'fail'

    return JsonResponse(data)