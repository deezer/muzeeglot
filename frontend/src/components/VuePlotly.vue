<template>
<div ref="container" class="vue-plotly"/>
</template>

<style scoped>
.vue-plotly {
  width: 100%;
  height: 100%;
}
</style>

<script>
import Plotly from 'plotly.js/dist/plotly.min.js' 
import debounce from 'lodash/debounce'
import defaults from 'lodash/defaults'

const events = [
  'click',
  'hover',
  'unhover',
  'selecting',
  'selected',
  'restyle',
  'relayout',
  'autosize',
  'deselect',
  'doubleclick',
  'redraw',
  'animated',
  'afterplot'
]

const functions = [
  'restyle',
  'relayout',
  'update',
  'addTraces',
  'deleteTraces',
  'moveTraces',
  'extendTraces',
  'prependTraces',
  'purge'
]

const methods = functions.reduce((all, funcName) => {
  all[funcName] = function(...args) {
    return Plotly[funcName].apply(Plotly, [this.$refs.container].concat(args))
  }
  return all
}, {})

export default {
  props: {
    options: {
      type: Object
    },
    data: {
      type: Array
    },
    layout: {
      type: Object
    }
  },
  data() {
    return {
      internalLayout: {
        ...this.layout,
        datarevision: 1
      }
    }
  },
  mounted() {
    this.react()
    this.initEvents()

    this.$watch('data', () => {
      this.internalLayout.datarevision++
      this.react()
    }, { deep: true })

    this.$watch('options', this.react, { deep: true })
    this.$watch('layout', this.relayout, { deep: true })
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.__resizeListener)
    this.__generalListeners.forEach(obj => this.$refs.container.removeAllListeners(obj.fullName))
    Plotly.purge(this.$refs.container)
  },
  methods: {
    initEvents() {
      this.__resizeListener = () => {
        this.internalLayout.datarevision++
        debounce(this.react, 200)
      }
      window.addEventListener('resize', this.__resizeListener)

      this.__generalListeners = events.map((eventName) => {
        return {
          fullName: 'plotly_' + eventName,
          handler: (...args) => {
            this.$emit.apply(this, [eventName].concat(args))
          }
        }
      })

      this.__generalListeners.forEach((obj) => {
        this.$refs.container.on(obj.fullName, obj.handler)
      })
    },
    ...methods,
    toImage(options) {
      let el = this.$refs.container
      let opts = defaults(options, {
        format: 'png',
        width: el.clientWidth,
        height: el.clientHeight
      })

      return Plotly.toImage(this.$refs.container, opts)
    },
    downloadImage(options) {
      let el = this.$refs.container
      let opts = defaults(options, {
        format: 'png',
        width: el.clientWidth,
        height: el.clientHeight,
        filename: (el.layout.title || 'plot') + ' - ' + new Date().toISOString()
      })

      return Plotly.downloadImage(this.$refs.container, opts)
    },
    plot() {
      return Plotly.plot(this.$refs.container, this.data, this.internalLayout, this.getOptions())
    },
    getOptions() {
      let el = this.$refs.container
      let opts = this.options

      // if width/height is not specified for toImageButton, default to el.clientWidth/clientHeight
      if (!opts) opts = {}
      if (!opts.toImageButtonOptions) opts.toImageButtonOptions = {}
      if (!opts.toImageButtonOptions.width) opts.toImageButtonOptions.width = el.clientWidth
      if (!opts.toImageButtonOptions.height) opts.toImageButtonOptions.height = el.clientHeight
      return opts
    },
    newPlot() {
      return Plotly.newPlot(this.$refs.container, this.data, this.internalLayout, this.getOptions())
    },
    react() {
      return Plotly.react(this.$refs.container, this.data, this.internalLayout, this.getOptions())
    }
  }
}
</script>