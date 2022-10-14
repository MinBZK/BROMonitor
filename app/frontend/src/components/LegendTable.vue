<template>
  <div :id="legendId" class="legend">
    <table class="broid-table">
      <tbody>
        <tr v-for="item in data" :key="item.title">
          <td>
            <q-icon name="stop" size="2rem" :style="{ color: item.colour }" />
          </td>
          <td>
            {{ item.title }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  props: {
    data: {
      type: Array,
      default() {
        return [];
      },
    },
    legendId: String,
  },
});
</script>
