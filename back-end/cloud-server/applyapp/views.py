from django.shortcuts import render
from django.http import JsonResponse
import os

# Create your views here.
def terraformApply(request):
    data = {"result" : 'success'}

    maintf = request.POST.get('iac')

    with open('main.tf', 'w') as f:
        f.write(maintf)
    
    commands = ['terraform init', 'terraform apply -auto-approve']

    for command in commands:
        if os.system(f'sudo {command}') == 0:
            continue    
        else:
            data["result"] = 'fail'
    
    return JsonResponse(data)