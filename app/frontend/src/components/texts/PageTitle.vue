<template>
  <h1 class="title col-12">{{ text }}</h1>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  props: {
    text: String,
  },
});
</script>
