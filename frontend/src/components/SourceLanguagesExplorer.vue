<template>
  <div class="source-languages-explorer">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">Source languages</v-list-item-title>
        <v-list-item-subtitle>{{ selected.length }} selected</v-list-item-subtitle>
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
        label="Select source language(s)"
        clearable chips dense multiple solo>
        <template v-slot:selection="data">
          <v-chip
            :input-value="data.selected"
            small
            class="ma-1"
            color="blue"
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
  name: "source-languages-select",
  computed: mapState({
    languages: state => state.supportedLanguages,
  }),
  created() {
    this.$store.dispatch('getLanguages');
  },
  data() {
    return {
      selected: [],
    };
  },
  watch: {
    selected (value) {
      this.$store.dispatch('setSelectedSourceLanguages', value);
    },
  }
};
</script>