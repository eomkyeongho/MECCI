from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import gpt
import os
import time
import random

# Create your views here.
def mutateCode(request):
    f = open("mecci-vue/src/assets/graph.svg", "w").close()
    data = {"origin": "", "mutated" : "", "diff" : ""}
    fileName = request.GET.get("filename")
    if fileName == "":
        return JsonResponse(data)
    
    data["mutated"], data["diff"] = gpt.mutateIaC(fileName)
    f = open("main.tf", 'w')
    f.write(data["mutated"])
    f.close()
    commands = ["terraform init", "terraform graph | dot -Tsvg > graph.svg", "move /Y graph.svg mecci-vue/src/assets/graph.svg", "del main.tf"]
    for command in commands:
        if os.system(command) == 0:
            continue
        else:
            print("os.system() error")
            break
    
    return JsonResponse(data)

def getOrigin(request):
    data = {"origin" : "", "filename" : ""}
    instance = request.GET.get("instance")
    if instance == 0 :
        return JsonResponse(data)
    
    files = [f for f in os.listdir("mutationapp/utils") if f"iac_{instance}_" in f]
    fileName = random.choice(files)
    print(f"selected {fileName}")
    tail = open(f"mutationapp/utils/{fileName}", mode='r')
    tail = tail.read()
    data["origin"] = gpt.head + tail
    data["filename"] = fileName

    return JsonResponse(data)

def validate(request):
    filename = request.GET.get("filename")
    filename = filename.replace('.tf', '')
    filename = filename.rstrip(filename[-1])

    files = [f for f in os.listdir("mutationapp/utils") if filename in f]
    index = 2

    while True:
        if f"{filename}{index}.tf" not in files:
            break
        index += 1

    if os.system(f"move /Y mutatedIaC mutationapp/utils/{filename}{index}.tf") == 0:
        print("Succefully add mutated code to the IaC pool")

    time.sleep(5)
    
    return HttpResponse("Succefully add mutated code to the IaC pool")

def showIaCList(request):
    files = ['📄' + f for f in os.listdir("mutationapp/utils") if ".tf" in f]
    files.remove('📄iac_head.tf')
    data = {}
    data["filelist"] = files
    
    return JsonResponse(data)
        
