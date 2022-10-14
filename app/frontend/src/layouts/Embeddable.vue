<template>
  <q-layout view="hhh lpr fff">
    <div class="row">
      <q-page-container
        class="offset-xs-0 col-xs-12 offset-md-2 col-md-8 q-px-xs-none q-px-lg-lg"
      >
        <slot />
      </q-page-container>
    </div>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>
