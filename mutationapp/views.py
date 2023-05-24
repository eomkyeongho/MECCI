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
    data = {}

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

    f = open('main.tf', 'w')
    f.write(data["mutated"])
    f.close()
    
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

def validateIaC(request):
    data = {}

    f = open('main.tf', 'r')
    iac = f.read()
    f.close()

    data["router"] = iac.count('"openstack_networking_router_v')
    data["subnet"] = iac.count('"openstack_networking_subnet_v')
    data["instance"] = iac.count('"openstack_compute_instance_v')
    
    fileName = f'r{data["router"]}_s{data["subnet"]}_i{data["instance"]}_infra'
    fileList = [f for f in os.listdir("mutationapp/iac") if ".tf" in f]

    index = 1

    while(True):
        if f'{fileName}{index}.tf' not in fileList:
            fileName = f'{fileName}{index}.tf'
            break
        index += 1

    f = open(fileName , 'w')
    f.write(iac)
    f.close()

    return JsonResponse(data)

