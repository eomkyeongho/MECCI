import hcl
import os

instanceDevices = ['openstack_compute_instance_v1', 'openstack_compute_instance_v2']
subnetDevices = ['openstack_networking_subnet_v1', 'openstack_networking_subnet_v2']
routerDevices = ['openstack_networking_router_v1', 'openstack_networking_router_v2']

def parseTerraform(path):
    with open(path, 'r') as f:
        maintf = hcl.load(f)

    resource = maintf["resource"]
    
    info = {"router" : 0, "subnet" : 0, "instance" : 0, "images": {}}

    for instanceDevice in instanceDevices:
        if instanceDevice in resource.keys():
            info["instance"] += len(resource[instanceDevice])
            for ins in resource[instanceDevice].keys():
                info["images"][ins] = resource[instanceDevice][ins]['image_id']   
    
    for subnetDevice in subnetDevices:
        if subnetDevice in resource.keys():
            info["subnet"] += len(resource[subnetDevice])
    
    for routerDevice in routerDevices:
        if routerDevice in resource.keys():
            info["router"] += len(resource[routerDevice])

    return info

def validate(path):
    return "validated"

def issueFileName(path, industry):
    info = parseTerraform(path)
    rout = info["router"]
    subn = info["subnet"]
    inst = info["instance"]

    fileName = f'r{rout}s{subn}i{inst}'
    
    fileList = [f.replace('.tf', '') for f in os.listdir("iac") if ".tf" in f]
    index = 1

    while(True):
        if f'{fileName}-{industry}-{index}' not in fileList:
            break
        index += 1
    
    fileName = f'{fileName}-{industry}-{index}'

    return fileName
    


