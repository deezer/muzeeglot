<template>
  <v-app>
    <v-navigation-drawer permanent left app>
      <source-languages-explorer></source-languages-explorer>
      <v-divider></v-divider>
      <target-language-explorer></target-language-explorer>
      <v-divider></v-divider>
      <musical-entity-explorer></musical-entity-explorer>
    </v-navigation-drawer>
    <v-content>
      <v-container class="pa-0 darkbg">
          <embedding-explorer></embedding-explorer>
          <v-divider></v-divider>
          <genres-explorer></genres-explorer>
      </v-container>
    </v-content>
  </v-app>
</template>

<style scoped>
.darkbg {
  background-color:#1e1e1e;
}
.theme--dark.v-application {
  background-color: #1e1e1e;
}
</style>

<script>
import EmbeddingExplorer from "@/components/EmbeddingExplorer.vue"
import SourceLanguagesExplorer from "@/components/SourceLanguagesExplorer.vue"
import TargetLanguageExplorer from "@/components/TargetLanguageExplorer.vue"
import MusicalEntityExplorer from "@/components/MusicalEntityExplorer.vue"
import GenresExplorer from "@/components/GenresExplorer.vue"

export default {
  name: 'Muzeeglot',
  components: {
      EmbeddingExplorer,
      SourceLanguagesExplorer,
      TargetLanguageExplorer,
      MusicalEntityExplorer,
      GenresExplorer,
  }
};
</script>
