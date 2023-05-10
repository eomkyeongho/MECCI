<template>
  <v-app>
    <v-app-bar class="py-2 px-5" color="light-blue-darken-4" density="compact">MECCI</v-app-bar>
    <v-container class= "mt-15" v-if = "render == 1">
        <v-card color="grey-lighten-2">
        <v-btn class="ma-1" color="grey-darken-1" @click="render = 0"> ← </v-btn>
        <div v-html="diff"></div>
    </v-card>
    </v-container>
    <v-container class= "mt-15" v-if = "render == 2">
        <v-card color="grey-lighten-2">
          <div>
            <v-btn class="ma-1" color="grey-darken-1" @click="render = 0"> ← </v-btn>
          </div>
          <v-img :src="require('./assets/graph.svg')"></v-img>
        </v-card>
    </v-container>
    <v-container  v-if = "render == 0" class="text-center mt-15">
        <v-row>
          <v-col cols="12" sm="5">
            <h3>Origin</h3>
            <v-textarea v-model="origin" rows="27" readonly></v-textarea>
            <v-row class="text-center">
              <v-col cols="12" sm="8"><v-select v-model="instance" items="123" label="instance"></v-select></v-col>
              <v-col cols="12" sm="4"><v-btn class="mt-2" v-on:click="getOrigin()">Generate</v-btn></v-col>
            </v-row>
          </v-col>
          <v-col cols="12" sm="5">
            <h3>Mutated</h3>
            <v-textarea v-model="mutated" rows="27" readonly></v-textarea>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select class = "mt-10 mx-10" v-model="vulnerability" items="OX" label="add vulnerability"></v-select>
            <v-btn class = "ma-5" color="green-lighten-2" v-on:click="mutate()" min-height="100" min-width="200">{{ mutating }}</v-btn>
            <v-btn v-if="isMutated" class = "ma-5" color="red-lighten-1" min-height="100" min-width="200" @click = "render = 1">Show Diff</v-btn>
            <v-btn v-if="isMutated" class = "ma-5" color="blue-darken-2" min-height="100" min-width="200" @click = "render = 2">Show Graph</v-btn>
            <v-btn v-if="isMutated" class = "ma-5" color="purple-darken-1" min-height="100" min-width="200" @click = "validate()">{{ validating}}</v-btn>
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
    iacParameters : [1,2,3],
    instance : 0,
    vulnerability : "X",
    render : 0,
    isMutated : false
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
      axios.get("/origin", {params: {instance : this.instance}})
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
        alert(res["data"])
        this.validating = "Validate"
      })
    }
  }
}
</script>
