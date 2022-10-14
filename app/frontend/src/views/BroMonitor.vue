<template>
  <q-page>
    <spinner :loaded="loaded" />
    <div
      v-if="
        loaded &&
          !urlContainsDate() &&
          Object(model).hasOwnProperty('static_data') &&
          Object.keys(model.static_data).length > 0
      "
      @click="handleClick"
    >
      <h1 style="color: red">{{ model.static_data["datumstempel"] }}</h1>
      <p>Klik op een regel voor meer informatie.</p>
      <div v-for="sectionKey in Object.keys(monitorItems)" :key="sectionKey">
        <q-separator class="divider" />
        <h2 tabindex="-1">{{ sectionKey }}</h2>
        <bro-monitor-item
          v-for="(mI, index) in monitorItems[sectionKey]"
          :sectionSideValue="mI['sectionSideValue']"
          :contentSelectors="mI['contentSelectors']"
          :title="mI['title']"
          :id="mI['id']"
          :model="model"
          :tabIndex="index"
          :iconName="mI['iconName']"
          :key="mI.item"
          :mapContent="mI['mapContent']"
        />
      </div>

      <q-separator class="divider" />
      <h2>En verder</h2>

      <bro-monitor-item
        :contentSelectors="['top20-registratieobjecten']"
        title="Top-20"
        id="expansion-item-top-20"
        :model="model"
        iconName="table_view"
      />

      <bro-monitor-item
        title="Trends"
        id="expansion-item-trends"
        :model="model"
        iconName="timeline"
      >
        <template v-slot:expanded-content>
          <p>Trends per gegevenstype in de BRO.</p>
          <div id="select-trends-wrapper">
            <label for="select-trends">Selecteer een ander type:</label>
            <select
              v-model="optionSelected"
              name="select-trends"
              class="select-trends"
              @change="changedObjecttype"
            >
              <option
                v-for="opt in trendOptions"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.label }}
              </option>
            </select>
          </div>

          <div v-html="model.static['bhrp-per-jaar-lijn']"></div>
          <div v-html="model.static['cpt-per-jaar-lijn']"></div>
          <div v-html="model.static['gmw-per-jaar-lijn']"></div>
          <div v-html="model.static['sfr-per-jaar-lijn']"></div>
          <div v-html="model.static['bhrgt-per-jaar-lijn']"></div>
          <div v-html="model.static['gmn-per-jaar-lijn']"></div>
          <div v-html="model.static['gld-per-jaar-lijn']"></div>
        </template>
      </bro-monitor-item>

      <bro-monitor-item
        :contentSelectors="['registratieobjecten-staaf']"
        title="Stand"
        id="expansion-item-stand"
        :model="model"
        iconName="bar_chart"
        :sectionSideValue="model.static_data['totaal_aantal_objecten']"
      />

      <bro-monitor-item
        :contentSelectors="['actualiteit']"
        title="Actualiteit van de gegevens"
        id="expansion-item-actualiteit"
        :model="model"
        iconName="source"
      />

      <div class="row justify-center">
        <img
          style="width: 48px !important"
          alt="BRO Logo"
          :src="require('@/assets/bro_logo.png').default"
        />
      </div>
    </div>
    <div
      v-if="
        loaded &&
          (urlContainsDate() || Object.keys(model.static_data).length === 0)
      "
      class="bromonitor row"
    >
      <div>
        <div class="text-primary" id="bromonitor-navigation">
          <a v-if="!isOldestMonitor()" href="#" @click="previousMonitor()">
            &lt; vorige
          </a>
          <span class="archive-link-inactive" v-else> vorige </span>
          |
          <router-link :to="{ name: 'bro-monitor-archive' }">
            naar archief
          </router-link>
          |
          <a v-if="!isMostRecentMonitor()" href="#" @click="nextMonitor()">
            volgende &gt;</a
          >
          <span class="archive-link-inactive" v-else> volgende</span>
        </div>
        <div
          id="archive-monitor"
          v-html="model.html"
          ref="monitor-html"
          @click="handleClick"
        ></div>
      </div>
    </div>
    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]"
      v-show="scY > 150"
    >
      <q-btn
        @click="toTop()"
        icon="vertical_align_top"
        aria-label="Ga naar de bovenkant van de pagina"
        color="primary"
        fab
      />
    </q-page-sticky>
  </q-page>
</template>
<script lang="ts">
import {
  getBromonitor,
  getBromonitorRecent,
  getBromonitorDates,
} from "@/api/bromonitor";
import Vue from "vue";

import {
  documentTypeLegendData,
  qualityRegimeLegendData,
} from "@/utils/legendData";
import LegendTable from "@/components/LegendTable.vue";
import BaseMapSvg from "@/views/reports/bronhoudermaps/BaseMapSvg.vue";
import {
  BromonitorModel,
  BromonitorModelRecent,
  BroMonitorItemModel,
} from "@/models/aggregate";
import BroMonitorItem from "@/views/BroMonitorItem.vue";

export default Vue.extend({
  components: {
    LegendTable,
    BaseMapSvg,
    BroMonitorItem,
  },
  data() {
    const dateOptions = {
      timeZone: "Europe/Amsterdam",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const loaded = false;
    const model: BromonitorModel | BromonitorModelRecent = {
      date: "",
      html: "",
    };
    const dates = [];
    const selectedDate = null;
    const objectLegendData = documentTypeLegendData;
    const regimeLegendData = qualityRegimeLegendData;
    const optionSelected = "cpt-per-jaar-lijn";
    const trendOptions = [
      { label: "BHR-GT", value: "bhrgt-per-jaar-lijn" },
      { label: "BHR-P", value: "bhrp-per-jaar-lijn" },
      { label: "CPT", value: "cpt-per-jaar-lijn" },
      { label: "GMN", value: "gmn-per-jaar-lijn" },
      { label: "GMW", value: "gmw-per-jaar-lijn" },
      { label: "GLD", value: "gld-per-jaar-lijn" },
      { label: "SFR", value: "sfr-per-jaar-lijn" },
    ];
    const scTimer = 0;
    const scY = 0;

    return {
      dateOptions,
      dates,
      selectedDate,
      loaded,
      model,
      objectLegendData,
      regimeLegendData,
      optionSelected,
      trendOptions,
      scTimer,
      scY,
    };
  },
  props: {
    date: String,
  },
  computed: {
    monitorItems() {
      const getStaticData = (key) => this.model["static_data"][key];

      const monitorItems: {
        [key: string]: Array<BroMonitorItemModel>;
      } = {
        "Afgelopen week": [
          {
            id: "expansion-item-actieve-bronhouders",
            iconName: "timeline",
            title: "Actieve bronhouders",
            sectionSideValue: getStaticData("aantal_bronhouders"),
            contentSelectors: ["animatie-graph-bronhouders"],
          },
          {
            id: "expansion-item-aantal-registraties",
            iconName: "bar_chart",
            title: "Aantal registraties",
            sectionSideValue: getStaticData("aantal_registraties"),
            contentSelectors: ["registratieobjecten-afgelopenweek-staaf"],
          },
          {
            id: "expansion-item-uitgelicht",
            iconName: "table_view",
            title: "Waarvan GLD",
            sectionSideValue: getStaticData("aantal_glds"),
            contentSelectors: ["glds-week", "glds-top-20"],
          },
        ],
        "Op de landkaart": [
          {
            id: "expansion-item-registratieobjecten-gemeenten",
            iconName: "map",
            title: "Gemeenten",
            sectionSideValue: getStaticData("aantal_gemeenten")[0],
            mapContent: {
              bronhouderType: "Gemeente",
              headerVariabele: "gemeenten",
              geojsonFile: "gemeentegrenzen.json",
              staticContent: this.model["static"],
              dataTypen: getStaticData("data_gemeente_typen"),
              dataRegimes: getStaticData("data_gemeente_regimes"),
            },
          },
          {
            id: "expansion-item-registratieobjecten-provincies",
            iconName: "map",
            title: "Provincies",
            sectionSideValue: getStaticData("aantal_provincies")[0],
            mapContent: {
              bronhouderType: "Provincie",
              className: "bromonitor-element",
              headerVariabele: "provincies",
              geojsonFile: "provinciegrenzen.json",
              staticContent: this.model["static"],
              dataTypen: getStaticData("data_provincie_typen"),
              dataRegimes: getStaticData("data_provincie_regimes"),
            },
          },
          {
            id: "expansion-item-registratieobjecten-waterschappen",
            iconName: "map",
            title: "Waterschappen",
            sectionSideValue: getStaticData("aantal_waterschappen")[0],
            mapContent: {
              bronhouderType: "Waterschap",
              headerVariabele: "waterschappen",
              geojsonFile: "waterschapsgrenzen.json",
              staticContent: this.model["static"],
              dataTypen: getStaticData("data_waterschap_typen"),
              dataRegimes: getStaticData("data_waterschap_typen"),
            },
          },
        ],
        // "En verder": [
        //   {
        //     id: "expansion-item-top-20",
        //     iconName: "table_view",
        //     title: "Top-20",
        //     contentSelectors: ["top20-registratieobjecten"],
        //   },
        // ],
      };
      return monitorItems;
    },
  },
  methods: {
    foo(value) {
      console.log(value);
    },
    toTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    handleScroll() {
      if (this.scTimer > 0) return;
      this.scTimer = window.setTimeout(() => {
        this.scY = window.scrollY;
        clearTimeout(this.scTimer);
        this.scTimer = 0;
      }, 100);
    },
    urlContainsDate() {
      return window.location.href.includes(this.$data.selectedDate);
    },
    isOldestMonitor() {
      const currentDateTime = this.$data.selectedDate + "T00:00:00";
      const currentIndex = this.$data.dates.indexOf(currentDateTime);
      return currentIndex == this.$data.dates.length - 1;
    },
    isMostRecentMonitor() {
      const currentDateTime = this.$data.selectedDate + "T00:00:00";
      const currentIndex = this.$data.dates.indexOf(currentDateTime);
      return currentIndex == 0;
    },
    previousMonitor() {
      const currentDateTime = this.$data.selectedDate + "T00:00:00";
      const currentIndex = this.$data.dates.indexOf(currentDateTime);
      const previousMonitorIndex = currentIndex + 1;
      const nextDate = this.$data.dates[previousMonitorIndex].split("T")[0];
      this.$router.push({
        name: "bro-monitor",
        query: { datum: nextDate },
      });
    },
    nextMonitor() {
      const currentDateTime = this.$data.selectedDate + "T00:00:00";
      const currentIndex = this.$data.dates.indexOf(currentDateTime);
      const nextMonitorIndex = currentIndex - 1;
      const nextDate = this.$data.dates[nextMonitorIndex].split("T")[0];
      this.$router.push({
        name: "bro-monitor",
        query: { datum: nextDate },
      });
    },
    loadBroMonitor() {
      const queryDate = this.$props.date;
      const queryDateTime = queryDate + "T00:00:00";

      const fetchData = async (): Promise<void> => {
        this.$data.dates = (await getBromonitorDates()).dates;
        let fetchMonitor;
        const index = this.$data.dates.indexOf(queryDateTime);

        // Date is found in the list, fetch that date
        if (queryDate && index != -1) {
          fetchMonitor = async (): Promise<void> => {
            if (index == 0) {
              this.$data.model = await getBromonitorRecent();
            } else {
              this.$data.model = await getBromonitor(queryDateTime);
            }
            this.$data.selectedDate = queryDate;
            this.$data.loaded = true;
          };
        }
        // Date does not exist, redirect
        else if (queryDate && index == -1) {
          this.$router.push({ name: "not-found" });
        }
        // No date given, fetch most recent
        else {
          fetchMonitor = async (): Promise<void> => {
            this.$data.model = await getBromonitorRecent();
            this.$data.selectedDate = this.$data.dates[0].split("T")[0];
            this.$data.loaded = true;
          };
        }
        fetchMonitor();
      };
      fetchData();
    },
    handleClick(e) {
      if (e.target.matches(".assistive-button")) {
        const idTable = e.target.id.substr(7);
        const element = document.getElementById(idTable);
        if (element != null) {
          if (!element.classList.contains("assistive")) {
            element.classList.add("assistive");
            element.classList.add("hidden");
            e.target.innerHTML = "Toon datatabel";
          } else {
            element.classList.remove("assistive");
            element.classList.remove("hidden");
            e.target.innerHTML = "Verberg datatabel";
          }
        }
      }
    },
    hideTrends() {
      this.trendOptions.forEach((option) => {
        const element = document.getElementById(option.value);
        if (element != null && option.value != this.optionSelected) {
          if (!element.classList.contains("hidden")) {
            element.classList.add("hidden");
          }
        }
      });
    },
    changedObjecttype() {
      this.hideTrends();
      const element = document.getElementById(this.$data.optionSelected);
      if (element != null) {
        if (element.classList.contains("hidden")) {
          element.classList.remove("hidden");
        }
      }
    },
  },
  watch: {
    date: function() {
      this.loadBroMonitor();
    },
  },
  mounted() {
    this.loadBroMonitor();
    window.addEventListener("scroll", this.handleScroll);
  },
  updated() {
    if (!this.urlContainsDate()) {
      this.hideTrends();
    }
  },
});
</script>
<style scoped>
#archive-monitor >>> .assistive-button {
  border-radius: 4px;
  border-color: black;
  color: black;
  margin: 16px;
  height: 38px;
  padding: 1px 16px;
  font-size: 14px;
  background-color: #f0f0f0 !important;
}

.archive-link-inactive {
  color: #666;
}

.trend-select {
  display: inline-block;
  width: 125px;
  margin-left: 4px;
  vertical-align: middle;
}
</style>
