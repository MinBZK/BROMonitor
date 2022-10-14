<template>
  <q-page>
    <div class="row">
        <div class="col-md-12" >
            <h5>Niet gevonden</h5>
            <q-separator color="primary"/>  
            <h6>De pagina die u heeft opgevraagd is niet gevonden.</h6>
            <p>Foutcode: 404</p>
        </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  setup() {
    return {};
  }
});
</script>
