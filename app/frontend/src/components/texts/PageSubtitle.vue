<template>
    <h2 class="subtitle col-xs-12 col-lg-6">{{ text }}</h2>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
    props: {
        text: String 
    }
});
</script>
