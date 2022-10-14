<template>
  <div class="col-xs-12 col-lg-6">
    <q-card class="card" square flat>
      <h1 v-if="title" class="home text-primary text-bold">{{ title }}</h1>
      <p>{{ text }}</p>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  props: {
    title: {
      type: String,
      default: "",
    },
    text: String,
  },
});
</script>
