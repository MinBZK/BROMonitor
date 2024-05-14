<template>
  <div class="markdown-body" v-html="fileContent"></div>
</template>

<script>
import { defineComponent, ref, watch } from "vue";
import showdown from "showdown";

export default defineComponent({
  props: {
    data: [String, Object],
  },
  setup(props) {
    const fileContent = ref("");
    const converter = new showdown.Converter();

    const updateContent = () => {
      let data = props.data;
      if (typeof data === 'object' && data.__esModule) {
        data = data.default;
      }
      fileContent.value = converter.makeHtml(data);
    };

    watch(() => props.data, updateContent, { immediate: true });

    return { fileContent };
  },
});
</script>