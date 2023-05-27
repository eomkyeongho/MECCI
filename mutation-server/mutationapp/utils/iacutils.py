import hcl

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
    return "temp"
    


