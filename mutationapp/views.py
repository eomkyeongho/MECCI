from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import gpt
import os
import time

# Create your views here.
def index(request):
    f = open("mecci-vue/src/assets/graph.svg", "w").close()
    data = {}
    data["origin"], data["mutated"], data["diff"] = gpt.mutationIaC()
    f = open("main.tf", 'w')
    f.write(data["mutated"])
    f.close()
    commands = ["terraform init", "terraform graph | dot -Tsvg > graph.svg", "move /Y graph.svg mecci-vue/src/assets/graph.svg", "del main.tf"]
    for command in commands:
        if os.system(command) == 0:
            continue
        else:
            print("ERROR")
            break
    
    return JsonResponse(data)
