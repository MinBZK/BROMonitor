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

import Vue from "vue";
export default Vue.extend({
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
