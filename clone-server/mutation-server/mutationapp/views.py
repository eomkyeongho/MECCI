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

    fileList = [f.replace('.tf', '') for f in os.listdir("iac") if ".tf" in f]
    
    data["fileList"] = fileList
    
    return JsonResponse(data)

def showIaCDetail(request):
    data = {}

    fileName = request.GET.get('fileName')

    try:
        iac = open(f'iac/{fileName}.tf', 'r')
        data["code"] = iac.read()
        iac.close()
    except:
        data["code"] = 'not exist'

    return JsonResponse(data) 

def randomChoiceIaC(request):
    data = {}

    fileList = [f for f in os.listdir("iac") if ".tf" in f]
    fileName = random.choice(fileList)

    data["fileName"] = fileName.replace('.tf', '')

    iac = open(f'iac/{fileName}', 'r')
    data["code"] = iac.read()
    iac.close()

    return JsonResponse(data)

def mutateIaC(request):
    data = {}
    
    with open("mutationapp/utils/stop_flag","w") as f:
         f.write("0")

    fileName = request.GET.get('fileName')

    data["origin"], data["mutated"] = gpt.mutateIaC(fileName)
    data["mutated"].replace("`","")
    
    with open("origin/main.tf","w") as f:
        f.write(data["origin"])
    
    with open('main.tf', 'w') as f:
        f.write(data["mutated"])
    
    return JsonResponse(data)

def terraformApply(request):
    data = {}

    try:
        with open('main.tf', 'r') as f:
            maintf = f.read()
        response = requests.post("http://121.135.134.175:8000/terraform-apply", data={'iac' : maintf})
        data["result"] = 'true'
    except:
        data["result"] = 'false'

    return JsonResponse(data)

def validateIaC(request):
    data = {"result" : 'validated'}

    commands = ['terraform init', 'terraform validate']

    for command in commands:
        if os.system(f'sudo {command}') == 0:
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
        data["message"] = 'file type must be .tf'
    else :
        industry = request.POST.get('industry')
        f = request.FILES.get('file')
        path = default_storage.save(name, ContentFile(f.read()))
        info = iacutils.parseTerraform(path)
        rout = info["router"]
        subn = info["subnet"]
        inst = info["instance"]

        fileName = f'r{rout}-s{subn}-i{inst}'

        fileList = [f.replace('.tf', '') for f in os.listdir("iac") if ".tf" in f]
        index = 1

        while(True):
            if f'{fileName}-{industry}-{index}' not in fileList:
                break
            index = index + 1
        
        fileName = f'{fileName}-{industry}-{index}'
        #fileName = iacutils.issueFileName(path ,industry)
        data["fileName"] = fileName

        if os.system(f'mv "{path}" "iac/{fileName}.tf"') == 0:
            with open(f'iac/{fileName}.tf', 'r') as f:
                data["code"] = f.read()

    return JsonResponse(data)


def injectVulnerability(request):
    data = {}

    shList = [sh for sh in os.listdir('.') if ".sh" in sh]

    with open('main.tf', 'r') as f:
        maintf = f.read()
    
    for sh in shList:
        if maintf.find(f'{sh}') == -1:
            continue
        else:
            script = sh
            while script == sh:
                script = random.choice(shList)
            maintf = maintf.replace(f'{sh}', f'{script}')
            break

    data["injected"] = maintf
    with open('tmp/injected.tf', 'w') as f:
        f.write(maintf)
    with open("main.tf","w") as f:
        f.write(maintf)

    return JsonResponse(data)


def choiceIaC(request):
    data = {}

    infraType=request.GET.get('infraType')
    routeNum=int(request.GET.get('routeNum'))
    subnetNum=int(request.GET.get('subnetNum'))
    instanceNum=int(request.GET.get('instanceNum'))
    imageType=request.GET.get('imageType')


    fileList = [f for f in os.listdir("iac") if ".tf" in f]
    fileAttribute={}

    for f in fileList:
        fileAttr=f.split('-')
        fRouteNum=int(fileAttr[0][1:])
        fSubnetNum=int(fileAttr[1][1:])
        fInstanceNum=int(fileAttr[2][1:])
        fInfra=fileAttr[3]

        key=(fRouteNum,fSubnetNum,fInstanceNum,fInfra)
        if key not in fileAttribute.keys():
            fileAttribute[key]=[]
        fileAttribute[key].append(f)

    try:
        fileName=random.choice(fileAttribute[(routeNum,subnetNum,instanceNum,infraType)])
        print(fileName)
        data["fileName"] = fileName.replace(".tf","")
        with open(f"iac/{fileName}","r") as iac:
            data["code"]=iac.read()
        data["result"]="true"
    except:
        data["result"]="false"

    return JsonResponse(data)


def visualizeIaC(request):
    data={}
    
    commands = ["docker run --rm -it  -v $(pwd)/origin:/src im2nguyen/rover -genImage true",
    "docker run --rm -it  -v $(pwd):/src im2nguyen/rover -genImage true",
    "rm -rf ./static/*.svg",
    "mv ./rover.svg ./static/mutated.svg",
    "mv ./origin/rover.svg ./static/origin.svg"]

    for command in commands:
        if os.system(f'sudo {command}') == 0:
            continue

    with open("./static/origin.svg","r") as f:
        data["origin_svg"]=f.read()

    with open("./static/mutated.svg","r") as f:
        data["mutated_svg"]=f.read()
    data["result"]="true"
    
    return JsonResponse(data)

def stopGenerating(request):
    data={}
    with open("mutationapp/utils/stop_flag","w") as f:
        f.write("1")
    data["result"]="true"
    return JsonResponse(data)