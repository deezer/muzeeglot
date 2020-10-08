<template>
  <div class="musical-entity-explorer-container">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">Musical entity</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <div class="pa-2">
      <v-autocomplete
        v-model="selectedMusicalEntity"
        :items="musicalEntities"
        :search-input.sync="search"
        :loading="searching"
        :menu-props="{'max-height':'250px'}"
        clearable
        hide-no-data hide-details
        item-value="eid"
        item-text="label"
        :placeholder="enabled ? 'Search for a musical entity' : 'Select languages first'"
        :disabled="!enabled"
        color="white"
        solo dense
        @click:clear="onClear">
      </v-autocomplete>
    </div>
    <div class="metadata pa-2 mt-8" v-if="eid != null">
      <v-card max-width="180">
        <v-img
            lazy-src="/images/missing.png"
            :src="cover"
            width="180" height="180"
            min-width="180" min-height="180"
            max-width="180" max-height="180"
            class="grey darken-4"></v-img>
      </v-card>
      <div class="localized-uris mt-2 pa-2">
        <a
            class="localized-uri"
            v-for="localized in metadata"
            :key="localized.locale"
            :href="localized.uri"
            target="_blank">
          {{ toFlag(localized.locale) }}&nbsp;
          <v-icon x-small>mdi-open-in-new</v-icon>
        </a>
    </div>
  </div>
</template>

<style scoped>
.metadata {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.localized-uris {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}
.localized-uri,
.localized-uri:active,
.localized-uri:visited,
.localized-uri:hover {
  margin: 2px;
  text-decoration: none;
}
</style>

<script>
import { mapState } from 'vuex'

export default {
  name: "musical-entity-explorer",
  computed: mapState({
    musicalEntities: state => state.musicalEntities,
    searching: state => state.searching,
    cover: state => state.selectedMusicalEntity.cover == null ? '/images/missing.png' : state.selectedMusicalEntity.cover,
    eid: state => state.selectedMusicalEntity.eid,
    label: state => state.selectedMusicalEntity.label,
    metadata: state => state.selectedMusicalEntity.metadata,
    enabled: state => state.selectedTargetLanguage != null && state.selectedSourceLanguages.length > 0
  }),
  data() {
    return {
      search: null,
      selectedMusicalEntity: null,
      localeMap: {
        'en': 'gb',
        'ja': 'jp',
        'cs': 'cz',
        'nl': 'nl',
        'fr': 'fr',
        'es': 'es'
      }
    };
  },
  watch: {
    search (query) {
      query && query !== this.selectedMusicalEntity && this.$store.dispatch('updateMusicalEntities', query);
    },
    selectedMusicalEntity (eid) {
      eid && this.$store.dispatch('setSelectedMusicalEntity', eid);
    },
    eid (value) {
      if (value == null) {
        this.search = null;
      }
    }
  },
  methods: {
    toFlag(locale) {
      let normalized = this.localeMap[locale];
      if (normalized == null) {
        normalized = locale;
      }
      return normalized.toUpperCase().replace(
        /./g,
        char => String.fromCodePoint(char.charCodeAt(0) + 127397));
    },
    onClear() {
      this.$store.commit('clearSelectedMusicalEntity');
    }
  }
};
</script>