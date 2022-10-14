<template>
  <q-header class="text-white" height-hint="198">
    <!-- <skip-link /> -->
    <rijksoverheid-logo />
    <div class="nav row bg-secondary nav-text q-px-xs-xs q-px-lg-lg">
      <breadcrumbs :class="cssOverride" />
    </div>
  </q-header>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";
import Breadcrumbs from "@/components/headers/Breadcrumbs.vue";
import RijksoverheidLogo from "@/components/headers/RijksoverheidLogo.vue";
import SkipLink from "@/components/headers/SkipLink.vue";

export default defineComponent({
  components: {
    Breadcrumbs,
    RijksoverheidLogo,
    SkipLink,
  },
  props: {
    cssOverride: {
      default:
        "offset-xs-0 col-xs-12 offset-md-2 col-md-8 q-px-xs-none q-px-lg-lg",
      type: String,
    },
  },
});
</script>
