
  terraform {
    required_version =">= 0.12"
    required_providers {
        openstack = {
            source     = "terraform-provider-openstack/openstack"
            version    = "~> 1.48.0"
        }
    }
}
provider openstack {
    user_name       = "admin"
    tenant_name     = "admin"
    password        = "secret"
    auth_url        = "http://172.30.1.17/identity"
}
# Image creation
resource "openstack_images_image_v2" "ubuntu1804" {
    name                = "ubuntu1804"
    local_file_path     = "/opt/stack/IaC/bionic-server-cloudimg-amd64.img"
    container_format    = "bare"
    disk_format         = "qcow2"
}
resource "openstack_images_image_v2" "cirros" {
    name                = "cirros"
    local_file_path     = "/opt/stack/IaC/cirros-0.5.2-x86_64-disk.img"
    container_format    = "bare"
    disk_format         = "qcow2"
}

resource "openstack_compute_instance_v2" "instance_3" {
    count            = 1
    name            = "instance_3"
    image_id        = openstack_images_image_v2.cirros.id
    flavor_id       = "42"

    network {
        name    = openstack_networking_network_v2.private_3.name
    }
	depends_on	= [openstack_networking_subnet_v2.subnet_3]
}


# Flavor creation
resource "openstack_compute_flavor_v2" "flavor_1" {
    name        = "flavor_1"
    ram         = "8192"
    vcpus       = "1"
    disk        = "20"
    flavor_id       = "flavor_1"
    is_public       = "true"
}

# Router creation
resource "openstack_networking_router_v2" "router_1" {
    name                = "router_1"
    external_network_id = "5b16677d-b429-4b7e-8edb-6e1c06020db3"
}
resource "openstack_networking_router_v2" "router_2" {
    name                = "router_2"
    external_network_id = "5b16677d-b429-4b7e-8edb-6e1c06020db3"
}

# Network creation
resource "openstack_networking_network_v2" "private_1"{
    name            = "private_1"
    admin_state_up    = true
}
resource "openstack_networking_network_v2" "private_2" {
    name            = "private_2"
    admin_state_up    = true
}
resource "openstack_networking_network_v2" "private_3" {
    name            = "private_3"
    admin_state_up    = true
}
resource "openstack_networking_network_v2" "private_4"{
    name            = "private_4"
    admin_state_up    = true
}

#Connect network to Router1
resource "openstack_networking_subnet_v2" "subnet_1" {
    name        = "subnet_1"
    network_id    = openstack_networking_network_v2.private_1.id
    cidr        = "10.0.0.0/24"
    ip_version        = 4
    dns_nameservers    = ["8.8.8.8","8.8.4.4"]
}
resource "openstack_networking_subnet_v2" "subnet_2" {
    name        = "subnet_2"
    network_id    =  openstack_networking_network_v2.private_2.id
    cidr        = "10.0.1.0/24"
    ip_version        = 4
}

resource "openstack_networking_subnet_v2" "subnet_3" {
    name        = "subnet_3"
    network_id    = openstack_networking_network_v2.private_3.id
    cidr        = "10.0.2.0/24"
    ip_version        = 4
}

resource "openstack_networking_subnet_v2" "subnet_4" {
    name        = "subnet_4"
    network_id    = openstack_networking_network_v2.private_4.id
    cidr        = "10.0.3.0/24"
    ip_version        = 4
}

resource "openstack_compute_instance_v2" "instance_2" {
    count            = 1
    name            = "instance_2"
    image_id        = openstack_images_image_v2.cirros.id
    flavor_id       = "42"

    network {
        name    = openstack_networking_network_v2.private_2.name
    }
	depends_on	= [openstack_networking_subnet_v2.subnet_2]
}


resource "openstack_networking_router_interface_v2" "interface_1"{
    router_id    = openstack_networking_router_v2.router_1.id
    subnet_id    = openstack_networking_subnet_v2.subnet_1.id
}
resource "openstack_networking_router_interface_v2" "interface_2" {
    router_id    = openstack_networking_router_v2.router_1.id
    subnet_id    = openstack_networking_subnet_v2.subnet_2.id
}
resource "openstack_networking_router_interface_v2" "interface_3" {
    router_id    = openstack_networking_router_v2.router_2.id
    subnet_id    = openstack_networking_subnet_v2.subnet_3.id
}
resource "openstack_networking_router_interface_v2" "interface_4" {
    router_id    = openstack_networking_router_v2.router_1.id
    subnet_id    = openstack_networking_subnet_v2.subnet_4.id
}

# Modified code with updated rules
resource "openstack_compute_secgroup_v2" "http" {
    name        = "http"
    description    = "Open input http port"
    rule {
        from_port    = 80
        to_port        = 80
        ip_protocol    ="tcp"
        cidr        ="0.0.0.0/0"
    }
}
resource "openstack_compute_secgroup_v2" "service" {
    name        = "service"
    description    = "Open input service port"
    rule {
        from_port    = 8080
        to_port        = 8080
        ip_protocol    = "tcp"
        cidr        = "0.0.0.0/0"
    }
}

resource "openstack_networking_port_v2" "http" {
    name                = "port-instance-http"
    network_id            = openstack_networking_network_v2.private_1.id
    admin_state_up        = true
    security_group_ids     = [
        openstack_compute_secgroup_v2.http.id,
        openstack_compute_secgroup_v2.service.id
    ]
    fixed_ip {
        subnet_id         = openstack_networking_subnet_v2.subnet_1.id
    }
}
resource "openstack_networking_floatingip_v2" "http"{
    pool = "public"
}

resource "openstack_compute_floatingip_associate_v2" "http" {
    floating_ip    = openstack_networking_floatingip_v2.http.address
    instance_id    = openstack_compute_instance_v2.instance_1.id
}

resource "openstack_compute_instance_v2" "instance_1" {
    name            = "instance_1"
    image_id        = openstack_images_image_v2.ubuntu1804.id
    flavor_id       = "flavor_1"

    user_data        = file("simple_webserver.sh")

    network {
        port        = openstack_networking_port_v2.http.id
    }
	depends_on		= [openstack_networking_port_v2.http]
}
# Add 0 instances with cirros image in the network
