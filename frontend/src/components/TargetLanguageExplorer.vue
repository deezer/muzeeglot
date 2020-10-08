<template>
  <div class="target-language-explorer">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">Target language</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <div class="pa-2">
      <v-select
        v-model="selected"
        :items="languages"
        :menu-props="{ maxHeight: '400' }"
        item-value="locale"
        item-text="label"
        hide-selected
        label="Select target language"
        clearable chips dense solo>
        <template v-slot:selection="data">
          <v-chip
            :input-value="data.selected"
            color="green"
            small
            text-color="white">
            <strong>{{ data.item.label }}</strong>&nbsp;
          </v-chip>
        </template>
      </v-select>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "target-language-select",
  computed: mapState({
    languages (state) {
      let values = [];
      state.supportedLanguages.forEach((language) => {
        if (state.selectedSourceLanguages.indexOf(language) == -1) {
          values.push(language);
        }
      });
      return values;
    }
  }),
  created() {
    this.$store.dispatch('getLanguages');
  },
  data() {
    return {
      selected: null,
    };
  },
  watch: {
    selected (value) {
      this.$store.dispatch('setSelectedTargetLanguage', value);
    },
  }
};
</script>