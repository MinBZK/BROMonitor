<template>
  <div id="app">
    <VueAnnouncer />
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script lang="ts">
import { Layout } from "@/layouts/layout";
import { computed, defineComponent } from "vue";
import { useRoute } from "vue-router";

export default defineComponent({
  setup() {
    const route = useRoute();
    const layout = computed(
      (): Layout => (route.meta.layout as Layout) || Layout.Default,
    );
    return {
      layout,
    };
  },
});
</script>

<style>
@import "~ol/ol.css";
</style>
