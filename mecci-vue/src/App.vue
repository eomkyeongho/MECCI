<template>
  <v-app>
    <v-app-bar color="light-blue-darken-4" density="compact">
      <v-app-bar-nav-icon>
        MECCI
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-container class= "mt-15" v-if="render == 1">
        <v-card color="grey-lighten-2">
        <v-btn class="ma-1" color="grey-darken-1" @click="render = 0"> ← </v-btn>
        Diff
        <div v-html="diff"></div>
    </v-card>
    </v-container>
    <v-container class= "mt-15" v-if="render == 2">
        <v-card color="grey-lighten-2">
          <div>
            <v-btn class="ma-1" color="grey-darken-1" @click="render = 0"> ← </v-btn>
            Graph
          </div>
          <pdf src="./assets/graph.pdf"></pdf>
        </v-card>
    </v-container>
      <v-container class= "mt-15" v-if="render == 3">
        <v-card color="grey-lighten-2">
          <div>
            <v-btn class="ma-1" color="grey-darken-1" @click="render = 0"> ← </v-btn>
            IaC List
            <v-list :items="fileList"></v-list>
          </div>
        </v-card>
    </v-container>
    <v-container  v-if="render == 0" class="text-center mt-15">
        <v-row>
          <v-col cols="12" sm="5">
            <h3>Origin</h3>
            <v-textarea v-model="origin" rows="20" readonly></v-textarea>
            <v-row class="text-center">
              <v-col cols="12" sm="8"><v-select v-model="instance" :items="['1 instance', '2 instances', '3 instances']" label="instance"></v-select></v-col>
              <v-col cols="12" sm="4"><v-btn class="mt-2" v-on:click="getOrigin()">Generate</v-btn></v-col>
            </v-row>
          </v-col>
          <v-col cols="12" sm="5">
            <h3>Mutated</h3>
            <v-textarea v-model="mutated" rows="20" readonly></v-textarea>
          </v-col>
          <v-col cols="12" sm="2" >
            <v-btn class = "mx-5 mt-10 mb-1" color="green-lighten-2" v-on:click="mutate()" min-height="50" min-width="200">{{ mutating }}</v-btn>
            <v-btn class = "mx-5 my-1" color="green-lighten-2" min-height="50" min-width="200" @click="render = 3; getIaCList();">IaC Pool</v-btn>
            <v-btn v-if="isMutated" class = "mx-5 my-1" color="red-lighten-1" min-height="50" min-width="200" @click="render = 1">Show Diff</v-btn>
            <v-btn v-if="isMutated" class = "mx-5 my-1" color="blue-darken-1" min-height="50" min-width="200" @click="render = 2">Show Graph</v-btn>
            <v-btn v-if="isMutated" class = "mx-5 my-1" color="blue-darken-1" min-height="50" min-width="200" @click="showTopology()">Show Topology</v-btn>
            <v-btn v-if="isMutated" class = "mx-5 my-1" color="purple-darken-1" min-height="50" min-width="200" @click="validate()">{{ validating }}</v-btn>
            <v-btn v-if="isMutated" class = "mx-5 my-1" color="purple-darken-1" min-height="50" min-width="200" @click="apply()">{{ applying }}</v-btn>
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
    origin : "",
    mutated : "",
    diff : "",
    mutating : "Mutate",
    validating : "Validate",
    filename : "",
    instance : 0,
    vulnerability : "Keep",
    render : 0,
    isMutated : false,
    fileList : [],
    applying : "Apply"
  }),
  methods:{
    mutate() {
      if(this.instance == 0) {
        return
      }
      this.mutating = "Proceeding...";
      this.mutated = "mutating...";
      this.diff = "";
      this.isMutated=false;
      axios.get('/mutate', {params: {filename : this.filename}})
      .then(res => {
        this.mutated = res["data"]["mutated"];
        this.diff = res["data"]["diff"];
        this.mutating = "Mutate";
        this.isMutated = true;
      })
    },
    getOrigin(){
      if (this.instance == 0) {
        return
      }
      axios.get("/origin", {params: {instance : this.instance[0]}})
      .then(res => {
        this.origin = res["data"]["origin"]
        this.filename = res["data"]["filename"]
        this.mutated = ""
      })
    },
    validate() {
      this.validating = "Validating..."
      axios.get("/validate", {params: {filename : this.filename}})
      .then(res => {
        alert(res["data"]);
        this.validating = "Validate";
      })
    },
    getIaCList() {
      axios.get("/iac-list")
      .then(res => {
        this.fileList = res["data"]["filelist"];
        console.log(this.fileList);
      })
    },
    showTopology() {
      window.open("http://121.135.134.175/dashboard/project/network_topology/#!#close");
    },
    apply() {
      this.applying = "applying...";
      axios.get("/apply")
      .then(res =>{
        alert(res["data"]);
        this.applying = "Apply";
      })
    }
  }
}
</script>
