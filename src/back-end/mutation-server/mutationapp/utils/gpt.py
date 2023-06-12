import openai
import random
import requests
import os
from pygments import highlight
from pygments.lexers import TerraformLexer
from pygments.formatters import HtmlFormatter
import socketio

stop_flag = False
sio = socketio.Client()
sio.connect("http://localhost:8083")

openai.api_key = os.getenv("OPENAI_API_KEY")

def mutateIaC(fileName):
    with open(f'iac/{fileName}.tf', mode='r') as f:
        origin = f.read()
    
    command = origin + '\nModify the above code under the following rules\n'

    #count=random.randint(2,3)
    count=1
    
    for i in range(count):
        command += 'Add one more openstack_networking_network_v2 block\n'
        command += 'Add one more openstack_networking_subnet_v2 block\n'
        command += f'Connect the network to a router 1. If it does not exist, Add it.\n'
        command += f'Add 1 instances with cirros image, depends_on, `flaver_id = "42"` and no user_data in the network\n'

    #command += 'Just Show me the code and don`t say anything'
    command += 'Only respond with entire code as plain text without code block syntax around it'
    mutated = ''
    print(command)
        
    for chunk in openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{command}"}],stream=True):
        with open("mutationapp/utils/stop_flag","r") as f:
            flag=int(f.read())
        if flag==1:
            break        
        content = chunk["choices"][0].get("delta",{}).get("content")
        
        if type(content)==str:
            mutated += content  
            sio.emit('sendMessage',{"data":content})

    
    mutated.replace('`','')
    return origin, mutated
    '''
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{command}"}],)
        assistant_content = completion.choices[0].message["content"].strip()
        mutated = assistant_content.replace("`","")
        print("length:",len(mutated))
        
    except:
        mutated = 'gpt tokken error'
    
    return origin, mutated
    '''