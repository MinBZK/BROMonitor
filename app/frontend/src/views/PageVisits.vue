<template>
  <q-page>
    <spinner :loaded="loaded" />
    <div class="row">
      <page-title text="Gebruiksstatistieken" />
      <page-subtitle text="Hoevaak worden paginas bezocht?" />
    </div>
    <div class="row" v-show="loaded">
      <div class="col-xs-12 col-lg-6">
        <h4>Bezoek afgelopen 7 dagen:</h4>
        <table>
          <thead>
            <th>Pagina</th>
            <th>Bezoeken</th>
          </thead>
          <tbody>
            <tr v-for="item in dataWeek" :key="item.key">
              <td>{{ item.key }}</td>
              <td>{{ item.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="col-xs-12 col-lg-6">
        <h4>Bezoek afgelopen 28 dagen:</h4>
        <table>
          <thead>
            <th>Pagina</th>
            <th>Bezoeken</th>
          </thead>
          <tbody>
            <tr v-for="item in dataMonth" :key="item.key">
              <td>{{ item.key }}</td>
              <td>{{ item.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { getPageVisits } from "@/api/pageVisits";
import { CountAggregate } from "@/models/aggregate";
import Vue from "vue";

export default Vue.extend({
  data() {
    const dataWeek: CountAggregate[] = [];
    const dataMonth: CountAggregate[] = [];
    const loaded = false;
    return { dataWeek, dataMonth, loaded };
  },
  methods: {
    loadData() {
      const fetchData = async (): Promise<void> => {
        this.$data.dataWeek = await getPageVisits(7);
        this.$data.dataMonth = await getPageVisits(28);
        this.$data.loaded = true;
      };
      fetchData();
    },
  },
  beforeMount() {
    this.loadData();
  },
});
</script>
