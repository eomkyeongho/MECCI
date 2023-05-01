terraform {
	required_version =">= 0.12"
	required_providers {
		openstack = {
			source 	= "terraform-provider-openstack/openstack"
			version	= "~> 1.48.0"
		}
	}
}

provider openstack {
	user_name		= "admin"
	tenant_name		= "admin"
	password		= "secret"
	auth_url		= "http://172.30.1.17/identity"
}

# Image creation
resource "openstack_images_image_v2" "ubuntu1404" {
	name				= "ubuntu1404"
	local_file_path		= "/opt/stack/IaC/trusty-server-cloudimg-amd64-disk1.img"
	container_format	= "bare"
	disk_format			= "qcow2"
}

# Router creation
resource "openstack_networking_router_v2" "router_1" {
	name				= "router_1"
	external_network_id	= "494c20a9-9995-42e2-b252-e8f3fa320b91"
}


# Network creation
resource "openstack_networking_network_v2" "private_1"{
	name			= "private_1"
	admin_state_up	= true
}

# Subnet creation
resource "openstack_networking_subnet_v2" "subnet_1" {
	name		= "subnet_1"
	network_id	= openstack_networking_network_v2.private_1.id
	cidr		= "10.0.0.0/24"
	ip_version	= 4
}

# Connect subnet and external network 
resource "openstack_networking_router_interface_v2" "interface_1"{
	router_id	= openstack_networking_router_v2.router_1.id
	subnet_id	= openstack_networking_subnet_v2.subnet_1.id
}
