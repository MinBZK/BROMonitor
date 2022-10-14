<template>
  <div>
    <h5 v-show="!loaded">{{ loadingText }}</h5>
    <q-inner-loading class="spinner" :showing="!loaded">
      <q-spinner size="4em" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
export default {
  props: {
    loaded: Boolean,
    loadingText: {
      type: String,
      default: "Pagina wordt geladen..."
    }
  }
};
</script>
<style scoped>
.spinner {
  z-index: 2;
}
</style>
