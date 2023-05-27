from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import gpt, iacutils
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
        with open('main.tf', 'r') as f:
            maintf = f.read()
        response = requests.post("http://121.135.134.175:8000/terraform-apply", data={'iac' : maintf})
        data["result"] = 'success'
    except:
        data["result"] = 'fail'

    return JsonResponse(data)

def validateIaC(request):
    data = {"result" : 'validated'}

    commands = ['terraform init']

    for command in commands:
        if os.system(command) == 0:
            continue
        else:
            data["result"] = 'fail'
            break

    if data["result"] == 'validated':
        data["result"] = iacutils.validate('main.tf')

    return JsonResponse(data)

def uploadFile(request):
    data = {}
    
    name = request.POST.get('name')
    if name.find('.tf') == -1 :
        data["debug"] = 'file type must be .tf'
    else :
        industry = request.POST.get('industry')
        f = request.FILES.get('file')
        path = default_storage.save('main.tf', ContentFile(f.read()))
        info = iacutils.parseTerraform(path)
        rout = info["router"]
        subn = info["subnet"]
        inst = info["instance"]

        fileName = f'r{rout}s{subn}i{inst}'

        fileList = [f.replace('.tf', '') for f in os.listdir("mutationapp/iac") if ".tf" in f]
        index = 1

        while(True):
            if f'{fileName}-{index}' not in fileList:
                break
        
        fileName = f'{fileName}-{industry}-{index}'
        #fileName = iacutils.issueFileName(path ,industry)
        data["fileName"] = fileName

        os.system(f'move "{path}" "mutationapp/iac/{fileName}.tf"')

    return JsonResponse(data)

