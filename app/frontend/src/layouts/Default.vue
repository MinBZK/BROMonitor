<template>
  <q-layout view="hhh lpr fff">
    <bro-header />
    <div class="row">
      <q-page-container
        class="offset-xs-0 col-xs-12 offset-md-2 col-md-8 q-px-xs-none q-px-lg-lg content-wrapper"
        id="content-wrapper"
        tabindex="-1"
      >
        <slot />
      </q-page-container>
    </div>
    <bro-footer />
  </q-layout>
</template>

<script lang="ts">
import BroHeader from "@/components/headers/Header.vue";
import BroFooter from "@/components/Footer.vue";
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  components: {
    BroHeader,
    BroFooter
  },
  setup() {
    return {};
  }
});
</script>
