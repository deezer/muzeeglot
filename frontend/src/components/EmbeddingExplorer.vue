<template>
  <div ref="container" class="vue-plotly embedding-container">
    <vue-plotly
      ref="plotly"
      v-if="embeddingsReady"
      :data="embeddings"
      :layout="layout"
      :options="options" />
    <div class="loading-container" v-if="!embeddingsReady">
      <v-progress-circular
        :indeterminate="true"
        rotate="0"
        size="50"
        width="4"
        color="white"></v-progress-circular>
      <span>Loading embeddings</span>
    </div>
  </div>
</template>

<style scoped>
.embedding-container {
  width: 100%;
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #555555;
}
.loading-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>

<script>
import { mapState } from 'vuex'
import VuePlotly from "@/components/VuePlotly.vue"

export default {
  components: {
    VuePlotly
  },
  computed: mapState({
    embeddingsReady: state => state.embeddingsReady,
    embeddings: state => state.embeddings
  }),
  mounted() {
    this.$store.dispatch('getEmbeddings');
  },
  data() {
    return {
      layout: {
        plot_bgcolor: "#555555",
        paper_bgcolor: "#555555",
        autosize: true,
        margin: {l: 0, r: 0, b: 0, t: 0},
        showlegend: true,
        legend: {
          orientation: "h",
          font: {color: '#ffffff'},
          bgcolor: '#363636',
          bordercolor: '#666666',
          borderwidth: 1,
          x: 0,
          y: 0,
          xanchor: 'left',
          yanchor: 'bottom'
        },
        scene: {
          aspectratio: {x: 1, y: 1, z: 1 },
          camera: {
            center: {x: 0, y: 0, z: 0},
            eye: {x: 0.8, y: 0.8, z: 0.8},
            up: {x: 0, y: 0, z: 1}
          },
          xaxis: {
            autorange: true,
            zeroline: false,
            showgrid: true,
            showline: true,
            autotick: true,
            ticks: "",
            showticklabels: false,
            title: {text: ""},
            gridcolor: '#363636',
            linecolor: '#111111'
          },
          yaxis: {
            autorange: true,
            zeroline: false,
            showgrid: true,
            showline: true,
            autotick: true,
            ticks: "",
            showticklabels: false,
            title: {text: ""},
            gridcolor: '#363636',
            linecolor: '#111111'
          },
          zaxis: {
            autorange: true,
            zeroline: false,
            showgrid: true,
            showline: true,
            autotick: true,
            ticks: "",
            showticklabels: false,
            title: {text: ""},
            gridcolor: '#363636',
            linecolor: '#111111'
          }
        },
      },
      options: {}
    }
  }
}
</script>