<template>
  <v-app>
    <v-app-bar class="py-2 px-5" color="light-blue-darken-4" density="compact">MECCI</v-app-bar>
    <v-container class= "mt-15" v-if = "showDiff == true">
        <v-card color="grey-lighten-2">
        <v-btn class="ma-1" color="grey-darken-1" @click="showDiff = false"> ← </v-btn>
        <div v-html="diff"></div>
    </v-card>
    </v-container>
    <v-container  v-if = "showDiff == false" class="text-center mt-15">
        <v-row>
          <v-col cols="12" sm="5">
            <h3>Origin</h3>
            <v-textarea v-model="origin" rows="30" readonly></v-textarea>
          </v-col>
          <v-col cols="12" sm="5">
            <h3>Mutated</h3>
            <v-textarea v-model="mutated" rows="30" readonly></v-textarea>
          </v-col>
          <v-col cols="12" sm="2">
            <v-btn class = "ma-5 mt-10" color="green-lighten-2" v-on:click="getData" min-height="100" min-width="200">Mutate</v-btn>
            <v-btn class = "ma-5" color="red-lighten-1" min-height="100" min-width="200" @click = "showDiff = true">Show Diff</v-btn>
          </v-col>
        </v-row>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    origin : "terraform {\n\trequired_version =\">= 0.12\"\n\trequired_providers {\n\t\topenstack = {\n\t\t\tsource \t= \"terraform-provider-openstack/openstack\"\n\t\t\tversion\t= \"~> 1.48.0\"\n\t\t}\n\t}\n}\n\nprovider openstack {\n\tuser_name\t\t= \"admin\"\n\ttenant_name\t\t= \"admin\"\n\tpassword\t\t= \"secret\"\n\tauth_url\t\t= \"http://172.30.1.17/identity\"\n}\n\n# Image creation\nresource \"openstack_images_image_v2\" \"ubuntu1404\" {\n\tname\t\t\t\t= \"ubuntu1404\"\n\tlocal_file_path\t\t= \"/opt/stack/IaC/trusty-server-cloudimg-amd64-disk1.img\"\n\tcontainer_format\t= \"bare\"\n\tdisk_format\t\t\t= \"qcow2\"\n}\n\n# Router creation\nresource \"openstack_networking_router_v2\" \"router_1\" {\n\tname\t\t\t\t= \"router_1\"\n\texternal_network_id\t= \"494c20a9-9995-42e2-b252-e8f3fa320b91\"\n}\n\n\n# Network creation\nresource \"openstack_networking_network_v2\" \"private_1\"{\n\tname\t\t\t= \"private_1\"\n\tadmin_state_up\t= true\n}\n\n# Subnet creation\nresource \"openstack_networking_subnet_v2\" \"subnet_1\" {\n\tname\t\t= \"subnet_1\"\n\tnetwork_id\t= openstack_networking_network_v2.private_1.id\n\tcidr\t\t= \"10.0.0.0/24\"\n\tip_version\t= 4\n}\n\n# Connect subnet and external network \nresource \"openstack_networking_router_interface_v2\" \"interface_1\"{\n\trouter_id\t= openstack_networking_router_v2.router_1.id\n\tsubnet_id\t= openstack_networking_subnet_v2.subnet_1.id\n}\n#Access group http\nresource \"openstack_compute_secgroup_v2\" \"http\"{\n\tname\t\t\t= \"http\"\n\tdescription\t\t= \"Open input http port\"\n\trule {\n\t\tfrom_port\t= 80\n\t\tto_port\t\t= 80\n\t\tip_protocol\t= \"tcp\"\n\t\tcidr\t\t= \"0.0.0.0/0\"\n\t}\n}\n\n#Access group ssh\nresource \"openstack_compute_secgroup_v2\" \"ssh\" {\n\tname\t\t\t= \"ssh\"\n\tdescription\t\t= \"Open input ssh port\"\n\trule {\n\t\tfrom_port\t= 22\n\t\tto_port\t\t= 22\n\t\tip_protocol\t= \"tcp\"\n\t\tcidr\t\t= \"0.0.0.0/0\"\n\t}\n}\n\n#Access group icmp\nresource \"openstack_compute_secgroup_v2\" \"icmp\" {\n\tname\t\t\t= \"icmp\"\n\tdescription\t\t= \"Open icmp\"\n\trule {\n\t\tfrom_port\t= -1\n\t\tto_port\t\t= -1\n\t\tip_protocol\t= \"icmp\"\n\t\tcidr\t\t= \"0.0.0.0/0\"\n\t}\n}\n\n#Create network port\nresource \"openstack_networking_port_v2\" \"http\" {\n\tname\t\t\t\t= \"port-instance-http\"\n\tnetwork_id\t\t\t= openstack_networking_network_v2.private_1.id\n\tadmin_state_up\t\t= true\n\tsecurity_group_ids \t= [\n\t\topenstack_compute_secgroup_v2.http.id,\n\t\topenstack_compute_secgroup_v2.ssh.id,\n\t\topenstack_compute_secgroup_v2.icmp.id\n\t]\n\tfixed_ip {\n\t\tsubnet_id \t\t= openstack_networking_subnet_v2.subnet_1.id\n\t}\n}\n\n#Create floating ip\nresource \"openstack_networking_floatingip_v2\" \"http\"{\n\tpool = \"public\"\n}\n\n#Attach floating ip to instance\nresource \"openstack_compute_floatingip_associate_v2\" \"http\" {\n\tfloating_ip\t= openstack_networking_floatingip_v2.http.address\n\tinstance_id\t= openstack_compute_instance_v2.instance_1.id\n}\n\n# Instance creation\nresource \"openstack_compute_instance_v2\" \"instance_1\" {\n\tname\t\t\t= \"instance_1\"\n\timage_id\t\t= openstack_images_image_v2.ubuntu1404.id\n\tflavor_id\t\t= \"2\"\n\n\tuser_data\t\t= file(\"test.sh\")\n\n\n\tnetwork {\n\t\tport\t\t= openstack_networking_port_v2.http.id\n\t}\n}",
    mutated : "",
    diff : "",
    showDiff : false
  }),
  methods:{
    getData() {
      axios.get('/mutation')
      .then(res => {
        this.mutated = res["data"]["mutated"];
        this.diff = res["data"]["diff"];
      })
    }
  }
}
</script>
