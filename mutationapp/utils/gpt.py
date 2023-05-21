import openai
import random
import requests

openai.api_key = "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"

protocolList = [ '"http"', '"https"', '"icmp"', '"ssh"', '"custom_port"', '"telnet"' ]

prefix = '만약 위 코드에서 `"openstack_compute_secgroup_v2" '
suffixes = ['` 블럭이 존재한다면, 해당 블럭을 제거해줘\n', '` 블럭이 존재하지 않는다면, 해당 블럭을 추가해줘\n']

head = open("mutationapp/utils/iac_head.tf", mode='r')
head = head.read()

def mutateIaC(fileName):
    tail = open(f"mutationapp/utils/{fileName}", mode='r')
    tail = tail.read()
    command = tail + "\n위 코드를 다음과 같은 규칙 하에 수정한 코드를 보여줘\n" 

    origin = head + tail
    mutation = f""

    protocols = []
    for i in range(5):
        protocol = random.choice(protocolList)
        if protocol not in protocols:
            protocols.append(protocol)

    for p in protocols:
        suffix = random.choice(suffixes)
        print(prefix + p + suffix)
        command += prefix + p + suffix
    
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
    diff = requests.post("https://api.diffchecker.com/public/text?output_type=html&email=rudgh9242@naver.com", json = data)
    
    return mutated, diff.text