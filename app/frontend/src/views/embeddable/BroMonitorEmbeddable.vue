<template>
  <q-page>
    <div v-if="loaded" class="bromonitor row" v-html="model.html" @click="handleClick"></div>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn @click="toTop()" fab icon="keyboard_arrow_up" color="primary" />
    </q-page-sticky>
  </q-page>
</template>

<script lang="ts">
import { getBromonitorEmbedded } from "@/api/bromonitor";
import Vue from "vue";

export default Vue.extend({
  data() {
    const loaded = false;
    const model = {};
    return { loaded, model };
  },
  methods: {
    toTop() {
      window.scrollTo(0, 0);
    },
    loadBroMonitor() {
      const fetchMonitor = async (): Promise<void> => {
        this.$data.model = await getBromonitorEmbedded();
        this.$data.loaded = true;
      };
      fetchMonitor();
    },
    handleClick(e) {
      if (e.target.matches(".assistive-button")) {
        const idTable = e.target.id.substr(7);
        const element = document.getElementById(idTable);
        if (element != null) {
          if (!element.classList.contains("assistive")) {
            element.classList.add("assistive");
            e.target.innerHTML = "Toon datatabel";
          } else {
            element.classList.remove("assistive");
            e.target.innerHTML = "Verberg datatabel";
          }
        }
      }
    }
  },
  beforeMount() {
    this.loadBroMonitor();
  },
  
});
</script>
