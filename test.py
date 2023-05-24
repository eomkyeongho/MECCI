import hcl

instanceDevices = ['openstack_compute_instance_v1', 'openstack_compute_instance_v2']
subnetDevices = ['openstack_networking_subnet_v1', 'openstack_networking_subnet_v2']
routerDevices = ['openstack_networking_router_v1', 'openstack_networking_router_v2']

def parseTerraform():
    f = open('main.tf', 'r')
    maintf = hcl.load(f)['resource']
    f.close()

    instance = 0
    router = 0
    subnet = 0
    instanceImages = {}

    for instanceDevice in instanceDevices:
        if instanceDevice in maintf.keys():
            instance += len(maintf[instanceDevice])
            for ins in maintf[instanceDevice].keys():
                instanceImages[ins] = maintf[instanceDevice][ins]['image_id']   
    
    for subnetDevice in subnetDevices:
        if subnetDevice in maintf.keys():
            subnet += len(maintf[subnetDevice])
    
    for routerDevice in routerDevices:
        if routerDevice in maintf.keys():
            router += len(maintf[routerDevice])

    return router, subnet, instance, instanceImages

print(parseTerraform())


