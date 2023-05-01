import openai
import random

openai.api_key = "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"

subCommandList = ['"openstack_compute_secgroup_v2" "icmp" 블럭 제거', '"openstack_compute_secgroup_v2" "http" 블럭 제거', '"openstack_compute_secgroup_v2" "https" 블럭 추가', '"openstack_compute_secgroup_v2" "telnet" 블럭 추가', '"openstack_compute_secgroup_v2" "custom_port" from_port=1111, to_port=1111인 블럭 추가']

head = open("mutationapp/utils/iac_head.tf", mode='r')
head = head.read()
tail = open("mutationapp/utils/iac.tf", mode='r')
tail = tail.read()

def mutationIaC():
    command = tail + "\n위 코드를 다음과 같은 규칙 하에 수정한 코드를 보여줘\n" 

    ret = f""

    commands = []
    for i in range(5):
        comm = random.choice(subCommandList)
        if comm not in commands:
            commands.append(comm)

    for c in commands:
        command += f"{c}\n"
    
    command += "단, 코드만 보여주고 아무 말도 하지 말아줘."

    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{command}"}])
        assistant_content = completion.choices[0].message["content"].strip()
        ret = f"{head + assistant_content}"
    except:
        ret = f"gpt error"

    return f"{head + tail}", ret

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