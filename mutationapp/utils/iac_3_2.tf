# 수정된 코드

#Access group http
resource "openstack_compute_secgroup_v2" "http"{
	name			= "http"
	description		= "Open input http port"
	rule {
		from_port	= 80
		to_port		= 80
		ip_protocol	= "tcp"
		cidr		= "0.0.0.0/0"
	}
}

#Access group ssh
resource "openstack_compute_secgroup_v2" "ssh" {
	name			= "ssh"
	description		= "Open input ssh port"
	rule {
		from_port	= 22
		to_port		= 22
		ip_protocol	= "tcp"
		cidr		= "0.0.0.0/0"
	}
}

#Access group icmp
resource "openstack_compute_secgroup_v2" "icmp" {
	name			= "icmp"
	description		= "Open icmp"
	rule {
		from_port	= -1
		to_port		= -1
		ip_protocol	= "icmp"
		cidr		= "0.0.0.0/0"
	}
}

#Access group custom_port
resource "openstack_compute_secgroup_v2" "custom_port" {
  name          = "custom_port"
  description   = "Open custom port"
  rule {
    from_port   = 8080
    to_port     = 8080
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

#Create network port
resource "openstack_networking_port_v2" "http" {
	name				= "port-instance-http"
	network_id			= openstack_networking_network_v2.private_1.id
	admin_state_up		= true
	security_group_ids 	= [
		openstack_compute_secgroup_v2.http.id,
		openstack_compute_secgroup_v2.ssh.id,
		openstack_compute_secgroup_v2.icmp.id,
    openstack_compute_secgroup_v2.custom_port.id
	]
	fixed_ip {
		subnet_id 		= openstack_networking_subnet_v2.subnet_1.id
	}
}

#Create floating ip
resource "openstack_networking_floatingip_v2" "http"{
	pool = "public"
}

#Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "http" {
	floating_ip	= openstack_networking_floatingip_v2.http.address
	instance_id	= openstack_compute_instance_v2.instance_1.id
}

# Instance creation
resource "openstack_compute_instance_v2" "instance_1" {
	name			= "instance_1"
	image_id		= openstack_images_image_v2.ubuntu1404.id
	flavor_id		= "2"

	user_data		= file("test.sh")


	network {
		port		= openstack_networking_port_v2.http.id
	}
}

resource "openstack_compute_instance_v2" "instance_2" {
	name			= "instance_2"
	image_id		= openstack_images_image_v2.ubuntu1404.id
	flavor_id		= "3"

	user_data		= file("test.sh")


	network {
		port		= openstack_networking_port_v2.http.id
	}
}

resource "openstack_compute_instance_v2" "instance_3" {
	name			= "instance_3"
	image_id		= openstack_images_image_v2.ubuntu1404.id
	flavor_id		= "4"

	user_data		= file("test.sh")


	network {
		port		= openstack_networking_port_v2.http.id
	}
}