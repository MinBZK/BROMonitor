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
import { computed, defineComponent } from "@vue/composition-api";

export default defineComponent({
  setup(props, context) {
    const layout = computed(
      (): Layout => context.root.$route.meta.layout || Layout.Default
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
