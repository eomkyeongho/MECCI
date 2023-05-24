import openai
import random
import requests

openai.api_key = "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"

def mutateIaC(fileName):
    f = open(f'mutationapp/iac/{fileName}.tf', mode='r')
    origin = f.read()
    f.close()

    command = origin + '\nModify the above code under the following rules\n'

    count=random.randint(1,3)
    
    for i in range(count):
        command += 'Add one more openstack_network_networking_v2 block\n'
        command += f'Connect the network to a router{random.randint(1,3)}\n'
        command += f'Add {random.randint(0,2)} instances with cirros image in the network\n'

    command += 'Just Show me the code and don`t say anything'

    mutated = ''
    diff = ''

    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{command}"}])
        assistant_content = completion.choices[0].message["content"].strip()
        assistant_content.replace("```","")
        mutated = assistant_content

        diff = {"left" : f"{origin}", "right" : f"{mutated}", "diff_level" : "word"}
        diff = requests.post("https://api.diffchecker.com/public/text?output_type=html&email=rudgh9242@naver.com", json = diff).text
    except:
        mutated = 'gpt tokken error'
    
    return mutated, diff