import openai
import random
import requests

openai.api_key = ""

subCommandList = ['만약 위 코드에 "openstack_compute_secgroup_v2" "https" 블럭이 없다면 해당 블럭을 추가해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "icmp" 블럭이 없다면 해당 블럭을 추가해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "ssh" 블럭이 없다면 해당 블럭을 추가해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "custom_port" 블럭이 없다면 해당 블럭을 추가해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "http" 블럭이 없다면 해당 블럭을 추가해줘',
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "telnet" 블럭이 없다면 해당 블럭을 추가해줘',
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "https" 블럭이 있다면 해당 블럭을 제거해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "icmp" 블럭이 있다면 해당 블럭을 제거해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "ssh" 블럭이 있다면 해당 블럭을 제거해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "custom_port" 블럭이 있다면 해당 블럭을 제거해줘', 
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "http" 블럭이 있다면 해당 블럭을 제거해줘',
                  '만약 위 코드에 "openstack_compute_secgroup_v2" "telnet" 블럭이 있다면 해당 블럭을 제거해줘']

head = open("mutationapp/utils/iac_head.tf", mode='r')
head = head.read()

def mutateIaC(fileName):
    tail = open(f"mutationapp/utils/{fileName}", mode='r')
    tail = tail.read()
    command = tail + "\n위 코드를 다음과 같은 규칙 하에 수정한 코드를 보여줘\n" 

    origin = head + tail
    mutation = f""

    commands = []
    for i in range(10):
        comm = random.choice(subCommandList)
        if comm not in commands:
            commands.append(comm)

    print(commands)

    for c in commands:
        command += f"{c}\n"
    
    command += "단, 코드만 보여주고 아무 말도 하지 말아줘."

    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{command}"}])
        assistant_content = completion.choices[0].message["content"].strip()
        f = open('mutatedIaC', 'w')
        f.write(assistant_content)
        f.close()
        mutated = f"{head + assistant_content}"
    except:
        mutated = f"Request Token Exceeded"

    data = {"left" : f"{origin}", "right" : f"{mutated}", "diff_level" : "word"}
    response = requests.post("https://api.diffchecker.com/public/text?output_type=html&email=rudgh9242@naver.com", json = data)
    
    return mutated, response.text

# while True:
#     try:
#         user_content = input("user : ")
#         messages.append({"role": "user", "content": f"{command}"})

#         completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

#         assistant_content = completion.choices[0].message["content"].strip()

#         messages.append({"role": "assistant", "content": f"{assistant_content}"})

#         print(f"GPT : {assistant_content}")
#     except KeyboardInterrupt:
#         break
#     except:
#         print("error!")