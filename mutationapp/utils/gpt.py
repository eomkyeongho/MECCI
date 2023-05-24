import openai
import random
import requests

openai.api_key = "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"

def mutateIaC(fileName):
    f = open(f'mutationapp/iac/{fileName}.tf', mode='r')
    origin = f.read()
    f.close()

    f = open(f'mutationapp/iac/industry.tf', mode='r')
    mutated = f.read()
    f.close()

    diff = {"left" : f"{origin}", "right" : f"{mutated}", "diff_level" : "word"}
    diff = requests.post("https://api.diffchecker.com/public/text?output_type=html&email=rudgh9242@naver.com", json = diff)
    
    return mutated, diff.text