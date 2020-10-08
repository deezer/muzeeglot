<template>
  <div class="genres-explorer-container">
    <v-tabs grow>
      <v-tabs-slider></v-tabs-slider>
      <v-tab href="#sources">source genres</v-tab>
      <v-tab href="#target">target genres</v-tab>
      <v-tab href="#predictions">predicted genres</v-tab>
      <v-tab-item value="sources" class="pa-3">
        <div v-if="hasEntity">
          <v-switch
              v-model="sourcesEmbeddingsEnabled"
              label="Highlight source genres embeddings">
          </v-switch>
          <v-chip
                class="ma-1"
                v-for="tag in sources"
                :key="tag"
                color="blue"
                text-color="white">
            <strong>{{ tag }}</strong>
          </v-chip>
        </div>
        <div v-if="!hasEntity">{{ noData }}</div>
      </v-tab-item>
      <v-tab-item value="target" class="pa-3">
        <div v-if="hasEntity">
          <v-switch
              v-model="targetEmbeddingsEnabled"
              label="Highlight target genres embeddings">
          </v-switch>
          <v-chip
                class="ma-1"
                v-for="tag in target"
                :key="tag"
                color="green"
                text-color="white">
            <strong>{{ tag }}</strong>
          </v-chip>
        </div>
        <div v-if="!hasEntity">{{ noData }}</div>
      </v-tab-item>
      <v-tab-item value="predictions" class="pa-3">
        <div v-if="predictionError != null" class="red--text">
            {{ predictionError }}
        </div>
        <div v-if="hasEntity && predictionError == null">
          <v-switch
              v-model="predictionsEmbeddingsEnabled"
              label="Highlight genre predictions embeddings">
          </v-switch>
          <v-chip
                class="ma-1"
                v-for="(tag, order) in predictions"
                :key="tag.value"
                :color="tag.expected ? 'green' : '#af4cab'"
                text-color="white">
            <v-avatar
                left
                :style="{
                    'background-color': tag.expected ? '#2a8d30' : '#8d2a89' 
                }"
                :class="{'darken-4': true}">
                {{ order + 1 }}
            </v-avatar>
            <strong>{{ tag.value }}</strong>
          </v-chip>
        </div>
        <div v-if="!hasEntity">{{ noData }}</div>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<style scoped>
.tagset {
  display: flex;
  flex-wrap: wrap;
}
</style>

<script>
import { mapState } from 'vuex'


export default {
  name: "genres-explorer",
  computed: mapState({
    predictionError: state => state.predictionError,
    predictions: state => state.predictions,
    hasEntity: state => state.selectedMusicalEntity.eid != null,
    sources: state => state.sourcesTags,
    target: state => state.targetTags
  }),
  data() {
    return {
      noData: 'Please select source language(s), a target language, and a musical entity.',
      sourcesEmbeddingsEnabled: true,
      targetEmbeddingsEnabled: true,
      predictionsEmbeddingsEnabled: true
    }
  },
  watch: {
    sourcesEmbeddingsEnabled (value) {
      this.$store.commit('setSourcesEmbeddings', value);
    },
    targetEmbeddingsEnabled (value) {
      this.$store.commit('setTargetEmbeddings', value);
    },
    predictionsEmbeddingsEnabled (value) {
      this.$store.commit('setPredictionsEmbeddingsEnabled', value);
    }
  }
};
</script>