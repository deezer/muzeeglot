import Vue from 'vue'
import Vuex from 'vuex'
import * as d3 from 'd3'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
      api: '/api',
      supportedLanguages: [],
      musicalEntities: [],
      searching: false,
      selectedSourceLanguages: [],
      selectedTargetLanguage: null,
      selectedMusicalEntity: {
        eid: null,
        label: null,
        metdata: [],
        cover: null,
      },
      sourcesTags: [],
      targetTags: [],
      predictions: [],
      embeddingsReady: false,
      embeddingsReverseIndex: {},
      embeddings: [
        {
          x: [],
          y: [],
          z: [],
          text: [],
          name: 'sources',
          mode: 'markers+text',
          type: 'scatter3d',
          showlegend: false,
          visible: true,
          marker: {
            color: '#2196f3',
            opacity: 0.4,
            size: 10,
            line: {
              color: 'rgba(217, 217, 217, 0.14)',
              width: 0.5
            }
          },
          textfont: {
            family: 'Verdana',
            size: 12,
            color: '#ffffff'
          }
        },
        {
          x: [],
          y: [],
          z: [],
          text: [],
          name: 'target',
          mode: 'markers+text',
          type: 'scatter3d',
          showlegend: false,
          visible: true,
          marker: {
            color: '#4caf50',
            opacity: 0.4,
            size: 10,
            line: {
              color: 'rgba(217, 217, 217, 0.14)',
              width: 0.5
            }
          },
          textfont: {
            family: 'Verdana',
            size: 12,
            color: '#ffffff'
          }
        },
        {
          x: [],
          y: [],
          z: [],
          text: [],
          name: 'matched prediction',
          mode: 'markers+text',
          type: 'scatter3d',
          showlegend: false,
          visible: true,
          marker: {
            color: '#4caf50',
            opacity: 0.4,
            size: 12,
            line: {
              color: 'rgba(217, 217, 217, 0.14)',
              width: 0.5
            }
          },
          textfont: {
            family: 'Verdana',
            size: 12,
            color: '#ffffff'
          }
        },
        {
          x: [],
          y: [],
          z: [],
          text: [],
          name: 'unmatched prediction',
          mode: 'markers+text',
          type: 'scatter3d',
          showlegend: false,
          visible: true,
          marker: {
            color: '#af4cab',
            opacity: 0.4,
            size: 10,
            line: {
              color: 'rgba(217, 217, 217, 0.14)',
              width: 0.5
            }
          },
          textfont: {
            family: 'Verdana',
            size: 14,
            color: '#ffffff'
          }
        }],
      colors: [
        'rgb(29, 113, 217)',
        'rgb(207, 96, 87)',
        'rgb(224, 254, 184)',
        'rgb(22, 252, 3)',
        'rgb(19, 9, 130)',
        'rgb(57, 107, 36)'
      ],
      predictionError: null,
      searchError: null,
  },
  mutations: {
      setSupportedLanguages (state, languages) {
        state.supportedLanguages = languages;
      },
      setSearching (state, value) {
        state.searching = value;
      },
      setSelectedSourceLanguages (state, sourceLanguages) {
        state.selectedSourceLanguages = sourceLanguages;
      },
      setSelectedTargetLanguage (state, targetLanguage) {
        state.selectedTargetLanguage = targetLanguage;
      },
      setSelectedMusicalEntity (state, musicalEntity) {
        state.selectedMusicalEntity = musicalEntity;
      },
      setSourcesEmbeddings(state, value) {
        state.embeddings[0].visible = value;
      },
      setTargetEmbeddings(state, value) {
        state.embeddings[1].visible = value;
      },
      setPredictionsEmbeddingsEnabled(state, value) {
        state.embeddings[2].visible = value;
        state.embeddings[3].visible = value;
      },
      setPredictionError(state, predictionError) {
        state.predictionError = predictionError;
      },
      setSearchError(state, searchError) {
        state.searchError = searchError;
      },
      setMusicalEntities (state, musicalEntities) {
        state.searchError = null;
        state.musicalEntities = musicalEntities;
      },
      setEmbeddings(state, embeddings) {
        state.embeddingsReady = true;
        for (let i = 0; i < embeddings.length; i++) {
          let localized = embeddings[i];
          state.embeddings.push(localized);
          for (let j = 0; j < localized.text.length; j++) {
              let tag = localized.text[j];
              state.embeddingsReverseIndex[tag] = {x: i + 4, y: j};
          }
        }
      },
      setHighlightedSourcesEmbeddings (state) {
        let sources = state.embeddings[0];
        sources.x, sources.y, sources.z, sources.text = [], [], [], [];
        state.sourcesTags.forEach((tag) => {
          let hit = state.embeddingsReverseIndex[tag];
          if (hit != null) {
            sources.x.push(state.embeddings[hit.x].x[hit.y]);
            sources.y.push(state.embeddings[hit.x].y[hit.y]);
            sources.z.push(state.embeddings[hit.x].z[hit.y]);
            sources.text.push(tag);
          }
        });
      },
      setHighlightedTargetEmbeddings (state) {
        let target = state.embeddings[1];
        target.x, target.y, target.z, target.text = [], [], [], [];
        state.targetTags.forEach((tag) => {
          let hit = state.embeddingsReverseIndex[tag];
          if (hit != null) {
            target.x.push(state.embeddings[hit.x].x[hit.y]);
            target.y.push(state.embeddings[hit.x].y[hit.y]);
            target.z.push(state.embeddings[hit.x].z[hit.y]);
            target.text.push(tag);
          }
        });
      },
      setHighlightedPredictionsEmbeddings (state) {
        let ps = state.embeddings[2];
        let pe = state.embeddings[3];
        ps.x, ps.y, ps.z, ps.text = [], [], [], [];
        pe.x, pe.y, pe.z, pe.text = [], [], [], [];
        state.predictions.forEach((prediction) => {
          let hit = state.embeddingsReverseIndex[prediction.value];
          if (hit != null) {
            let sink = prediction.expected ? ps : pe;
            sink.x.push(state.embeddings[hit.x].x[hit.y]);
            sink.y.push(state.embeddings[hit.x].y[hit.y]);
            sink.z.push(state.embeddings[hit.x].z[hit.y]);
            sink.text.push(prediction.value);
          }
        });
      },
      setSourcesTags(state) {
        state.sourcesTags = [];
        state.selectedMusicalEntity.metadata.forEach((localized) => {
          if (state.selectedSourceLanguages.indexOf(localized.locale) != -1) {
            localized.tags.forEach((tag) => state.sourcesTags.push(tag));
          }
        });
      },
      setTargetTags(state) {
        state.targetTags = []
        state.selectedMusicalEntity.metadata.forEach((localized) => {
          if (state.selectedTargetLanguage == localized.locale) {
            localized.tags.forEach((tag) => state.targetTags.push(tag));
          }
        });
      },
      setPredictions(state, predictions) {
        let alignedPredictions = []
        predictions.forEach((prediction) => {
          alignedPredictions.push({
            value: prediction,
            expected: state.targetTags.indexOf(prediction) != -1
          });
        });
        state.predictionError = null;
        state.predictions = alignedPredictions;
      },
      clearSelectedMusicalEntity (state) {
        state.selectedMusicalEntity.eid = null;
        state.selectedMusicalEntity.label = null;
        state.selectedMusicalEntity.metdata = [];
        state.selectedMusicalEntity.cover = null;
        for (let i = 0; i < 4; i++) {
            state.embeddings[i].x = [];
            state.embeddings[i].y = [];
            state.embeddings[i].z = [];
            state.embeddings[i].text = [];
        }
        state.sourcesTags = [];
        state.targetTags = [];
        state.predictions = [];
      },
  },
  actions: {
      async getLanguages ({ commit, state }) {
        let response = await fetch(`${state.api}/languages`);
        let languages = await response.json();
        commit('setSupportedLanguages', languages)
      },
      async getEmbeddings ({ commit, state }) {
        let data = await d3.csv(`${state.api}/embeddings`);
        let embeddings = {};
        let locales = [];
        let color = 0;
        data.forEach(row => {
            let locale = row.tag.substring(0, 2);
            if (locales.indexOf(locale) == -1) {
              locales.push(locale);
              embeddings[locale] = {
                x: [], y: [], z: [], text: [],
                mode: 'markers',
                type: 'scatter3d',
                name: locale,
                marker: {
                  color: state.colors[color++],
                  size: 2
                }
              }
            }
            embeddings[locale].x.push(row.x);
            embeddings[locale].y.push(row.y);
            embeddings[locale].z.push(row.z);
            embeddings[locale].text.push(row.tag);
        });
        let flattened = []
        locales.forEach((locale) => flattened.push(embeddings[locale]));
        commit('setEmbeddings', flattened);
      },
      async setSelectedSourceLanguages ({ commit, dispatch }, sourceLanguages) {
        commit('clearSelectedMusicalEntity');
        commit('setSelectedSourceLanguages', sourceLanguages);
        dispatch('getPredictions');
      },
      async setSelectedTargetLanguage ({ commit, dispatch }, targetLanguage) {
        commit('clearSelectedMusicalEntity');
        commit('setSelectedTargetLanguage', targetLanguage);
        dispatch('getPredictions');
      },
      async setSelectedMusicalEntity ({ commit, dispatch, state }, eid) {
        let response = await fetch(`${state.api}/entity/${eid}`);
        let entity = await response.json();
        let label = state.musicalEntities.find(
            (musicalEntity) => musicalEntity.eid == eid);
        if (label != null) {
            label = label.label;
        }
        commit('setSelectedMusicalEntity', {
          'eid': eid,
          'label': label,
          'metadata': entity.metadata,
          'cover': entity.cover
        });
        commit('setSourcesTags');
        commit('setTargetTags')
        commit('setHighlightedSourcesEmbeddings');
        commit('setHighlightedTargetEmbeddings');
        dispatch('getPredictions');
      },
      async getPredictions ({ commit, state }) {
       if (
            state.selectedSourceLanguages.length == 0
            || state.selectedTargetLanguage == null
            || state.selectedMusicalEntity.eid == null) {
          return;
        }
        let response = await fetch(`${state.api}/predict`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            'sources': state.selectedSourceLanguages,
            'target': state.selectedTargetLanguage,
            'eid': state.selectedMusicalEntity.eid
          })
        });
        if (response.ok) {
          commit('setPredictions', await response.json());
          commit('setHighlightedPredictionsEmbeddings');
        }
        else {
          commit('setPredictionError', await response.json());
        }
      },
      async updateMusicalEntities ({ commit, state }, query) {
          if (state.selectedTargetLanguage == null || state.selectedSourceLanguages.length ==0)
            return;
          commit('setSearching', true);
          let response = await fetch(`${state.api}/search`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              'query': query,
              'sources': state.selectedSourceLanguages,
              'target': state.selectedTargetLanguage
            })
          });
          if (response.ok) {
            commit('setMusicalEntities', await response.json());
            commit('setSearching', false);
          }
          else {
            commit('setSearchError', await response.json());
          }
      },
  },
  modules: {}
})
