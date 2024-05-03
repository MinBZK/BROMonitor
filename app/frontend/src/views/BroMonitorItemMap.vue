<template>
  <base-map-svg
    :bronhouderType="bronhouderType"
    :headerVariable="headerVariabele"
    :geojsonFile="geojsonFile"
    overlayMode="objecttypen"
    :staticContent="staticContent"
    :dataTypen="dataTypen"
    :dataRegimes="dataRegimes"
    :class="className || ''"
  />
</template>

<script lang="ts">
import BaseMapSvg from "@/views/reports/bronhoudermaps/BaseMapSvg.vue";

import { defineComponent } from "vue";

export default defineComponent({
  name: "BroMonitorItemMap",
  components: {
    BaseMapSvg,
  },
  props: {
    bronhouderType: String,
    headerVariabele: String,
    geojsonFile: String,
    staticContent: Object,
    dataTypen: Array,
    dataRegimes: Array,
    className: String,
  },
});
</script>
