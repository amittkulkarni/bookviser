<template>
  <canvas ref="canvas"></canvas>
</template>

<script>
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);
export default {
  props: {
    data: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      required: false,
      default: () => ({})
    }
  },
  mounted() {
    new Chart(this.$refs.canvas, {
      type: 'line', // Change this to 'line', 'pie', etc.
      data: this.data,
      options: this.options
    });
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>
