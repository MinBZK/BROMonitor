<template>
  <q-page>
    <div class="row">
      <div class="col-md-12">
        <h1>Sitemap</h1>
        <q-separator color="primary" />
        <p>
          Deze sitemap pagina toont een overzicht van de op deze website
          beschikbare pagina's.
        </p>
        <ul>
          <li>
            <router-link :to="{ name: 'bro-monitor' }"> Home</router-link>
          </li>
          <li>
            <router-link :to="{ name: 'bro-monitor-archive' }">
              Archief</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'gegevens-per-bronhouder' }">
              Download gegevens per bronhouder</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'cookies_privacy' }">
              Cookies en privacy</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'kwetsbaarheid-melden' }">
              Kwetsbaarheid-melden</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'overdebromonitor' }">
              Over de BRO Monitor</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'toegankelijkheid' }">
              Toegankelijkheid</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>
