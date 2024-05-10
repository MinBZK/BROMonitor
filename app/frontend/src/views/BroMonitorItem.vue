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
            :aria-expanded="expanded"
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
          :key="cS as string"
          style="padding: 0; margin: 0"
        >
          <br v-if="index > 0" :key="typeof cS === 'string' ? cS : undefined" />
          <div v-if="model && 'static' in model" v-html="model.static[cS as string]"></div>
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

import { defineComponent, onMounted, ref, nextTick } from "vue";

export default defineComponent({
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
  setup() {
    const expanded = ref(false);
    const expansion = ref(null);

    onMounted(async () => {
      await nextTick();
      if (expansion.value) {
        const expansionElement = (expansion.value as HTMLElement);
        const nestedDivs = expansionElement.querySelectorAll('div[tabindex="0"]');
        nestedDivs.forEach((div) => {
          div.setAttribute("tabIndex", "-1");
        });
      }
    });

    return {
      expanded,
      expansion
    };
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