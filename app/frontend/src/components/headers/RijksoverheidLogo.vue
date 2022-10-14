<template>
  <div class="row bg-white justify-center header-white">
    <div class="logo">
      <div class="wrapper">
        <img
          alt="Rijksoverheid Logo"
          :src="require(`@/assets/${logoSize()}`).default"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  methods: {
    logoSize() {
      return this.$q.screen.lt.md ? "logo-fallback-ro.svg" : "logo-ro.svg";
    }
  }
});
</script>

<style scoped>
.logo {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
}

.wrapper {
  display: flex;
  flex-basis: 100%;
  flex-wrap: wrap;
  max-width: 1200px;
  align-items: flex-start;
  justify-content: flex-start;
  margin-right: -16px;
  margin-left: -16px;
  justify-content: center;
}

.logo .wrapper img {
  margin-left: -50px;
  width: inherit;
  max-width: 1168px;
  -webkit-transform: translateX(50%);
  transform: translateX(50%);
}
</style>
