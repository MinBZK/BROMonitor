<template>
  <q-page>
    <div class="row">
      <div class="col-12">
        <page-title :text="$t('bromonitor_archief.titel')" />
        <page-subtitle :text="$t('bromonitor_archief.subtitel')" />
      </div>
    </div>
    <div class="row">
      <p class="col-12">Volledig archief:</p>
    </div>
    <div class="row archief-wrapper">
      <select
        aria-label="datum selectie lijst"
        name="archive-select"
        id="archive-select"
        v-model="date"
        @change="redirectToDateMonitor()"
      >
        <option
          v-for="opt in this.$data.selectOptions"
          :key="opt.value"
          :value="opt.value"
          >{{ opt.label }}</option
        >
      </select>
    </div>
    <div class="row">
      <div class="col-12">
        <p>Meest recente monitors:</p>
        <ul class="topicCols">
          <li v-for="index in 5" :key="index">
            <router-link
              v-if="dates.length > index - 1"
              :to="{
                name: 'bro-monitor',
                query: { datum: formatDate(dates[index - 1].value) },
              }"
              target="_blank"
            >
              <a class="text-primary"
                ><q-icon color="primary" name="keyboard_arrow_right" />
                {{ dates[index - 1].label }}
              </a>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
    <div class="row">
      <textbox :text="$t('bromonitor_archief.uitleg')" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { getBromonitorDates } from "@/api/bromonitor";
import Vue from "vue";

export default Vue.extend({
  data() {
    const dates = [];
    let date;
    const selectOptions = [];
    const loaded = false;
    return { dates, selectOptions, date };
  },
  methods: {
    getDates() {
      const dateOptions = {
        timeZone: "Europe/Amsterdam",
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      const fetchDatesData = async (): Promise<void> => {
        this.$data.dates = (await getBromonitorDates()).dates.map(
          (d: Date) => ({
            label: new Date(d).toLocaleString("nl-NL", dateOptions),
            value: d,
          })
        );
        this.$data.date = this.$data.dates[0];
        this.$data.selectOptions = this.$data.dates.map((x) => ({
          label: x.label,
          value: this.formatDate(x.value),
        }));
      };
      fetchDatesData();
    },
    formatDate(dateString) {
      return dateString.split("T")[0];
    },
    redirectToDateMonitor() {
      if (this.$data.date) {
        this.$router.push({
          name: "bro-monitor",
          query: { datum: this.$data.date },
        });
      }
    },
  },
  beforeMount() {
    this.getDates();
  },
});
</script>
<style scoped>
.archief-wrapper {
  padding-bottom: 1rem;
}
</style>
