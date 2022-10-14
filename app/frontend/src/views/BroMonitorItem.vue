<template>
  <q-expansion-item dense ref="expansion" v-model="expanded">
    <template v-slot:header>
      <q-item-section avatar>
        <q-icon :name="iconName" color="primary" size="24px" />
      </q-item-section>
      <q-item-section>
        <h3>
          <button
            class="button-text-only"
            :aria-expanded="expanded.toString()"
            aria-role="button"
            :id="id"
            @keyup.enter="(e) => e.preventDefault()"
            @keydown.enter="(e) => e.preventDefault()"
          >
            {{ title }}
          </button>
        </h3>
      </q-item-section>
      <q-item-section side>
        <b>{{ sectionSideValue }}</b>
      </q-item-section>
    </template>
    <q-card>
      <q-card-section>
        <div
          v-for="(cS, index) in contentSelectors"
          :key="cS"
          style="padding: 0; margin: 0"
        >
          <br v-if="index > 0" :key="cS" />
          <div v-html="model.static[cS]"></div>
        </div>
        <bro-monitor-item-map
          v-if="mapContent"
          :bronhouderType="mapContent['bronhouderType']"
          :headerVariabele="mapContent['headerVariabele']"
          :geojsonFile="mapContent['geojsonFile']"
          :staticContent="mapContent['staticContent']"
          :dataTypen="mapContent['dataTypen']"
          :dataRegimes="mapContent['dataRegimes']"
          :className="mapContent['className']"
        />
        <slot name="expanded-content" />
      </q-card-section>
      <hr role="presentation" />
    </q-card>
  </q-expansion-item>
</template>
  
  <script lang="ts">
import BroMonitorItemMap from "@/views/BroMonitorItemMap.vue";
import BaseMapSvg from "@/views/reports/bronhoudermaps/BaseMapSvg.vue";

import Vue from "vue";
export default Vue.extend({
  name: "BroMonitorItem",
  components: {
    BroMonitorItemMap,
    BaseMapSvg,
  },
  props: {
    sectionSideValue: String,
    contentSelectors: Array,
    title: String,
    model: Object,
    id: String,
    iconName: String,
    tabIndex: Number,
    mapContent: Object,
  },
  data() {
    return {
      expanded: false,
    };
  },
  mounted() {
    // q-expansion-item introduces nested divs with a tabindex.
    // For accessability, the tab should be directly on the element that has an interaction, in this case <button>.
    // Therefore, the tabindex on nested divs should be removed.
    const expansionItem: any = this.$refs.expansion;
    expansionItem.$children.map((c) => {
      if (c.$el.tabIndex == 0) {
        c.$el.setAttribute("tabIndex", -1);
      }
    });
  },
});
</script>
  
  <style scoped>
.button-text-only {
  background: none !important;
  border: none;
  padding: 0 !important;
  cursor: pointer;
}
</style>