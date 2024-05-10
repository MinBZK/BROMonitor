<template>
  <q-page>
    <spinner :loaded="loaded" />
    <div
      v-if="
        loaded &&
        !urlContainsDate() &&
        model &&
        'static_data' in model &&
        Object(model).hasOwnProperty('static_data') &&
        Object.keys(model.static_data).length > 0
      "
      @click="handleClick"
    >
      <h1 class="red-text">
        {{
          model && "static_data" in model && model.static_data["datumstempel"]
        }}
      </h1>
      <p>Klik op een regel voor meer informatie.</p>
      <q-separator class="divider" />
      <h2>Afgelopen week</h2>
      <q-expansion-item
        id="expansion-item-actieve-bronhouders"
        dense
        v-model="actieveBronhoudersExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="actieveBronhoudersExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="timeline" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Actieve bronhouders</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_bronhouders"]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['animatie-graph-bronhouders']"
            ></div>
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        id="expansion-item-aantal-registraties"
        v-model="aantalRegistratiesExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="aantalRegistratiesExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="bar_chart" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Aantal registraties</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_registraties"]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['registratieobjecten-afgelopenweek-staaf']"
            ></div>
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item id="expansion-item-uitgelicht" v-model="gldExpanded">
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="gldExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="table_view" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Waarvan GLD</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_glds"]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['glds-week']"
            ></div>
            <br />
            <div
              v-if="model && 'static' in model"
              v-html="model.static['glds-top-20']"
            ></div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-separator class="divider" />
      <h2 style="padding-top: 20px">Op de landkaart</h2>
      <q-expansion-item
        id="expansion-item-registratieobjecten-gemeenten"
        v-model="gemeentenExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="gemeentenExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="map" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Gemeenten</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_gemeenten"][0]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <base-map-svg
              bronhouderType="Gemeente"
              headerVariable="gemeenten"
              geojsonFile="gemeentegrenzen.json"
              overlayMode="objecttypen"
              v-if="model && 'static' in model"
              :staticContent="model.static"
              :dataTypen="model.static_data['data_gemeente_typen']"
              :dataRegimes="model.static_data['data_gemeente_regimes']"
            />
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        id="expansion-item-registratieobjecten-provincies"
        v-model="provinciesExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="provinciesExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="map" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Provincies</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_provincies"][0]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <base-map-svg
              class="bromonitor-element"
              bronhouderType="Provincie"
              headerVariable="provincies"
              geojsonFile="provinciegrenzen.json"
              overlayMode="objecttypen"
              v-if="model && 'static' in model"
              :staticContent="model.static"
              :dataTypen="model.static_data['data_provincie_typen']"
              :dataRegimes="model.static_data['data_provincie_regimes']"
            />
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        id="expansion-item-registratieobjecten-waterschappen"
        v-model="waterschappenExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="waterschappenExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="map" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Waterschappen</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["aantal_waterschappen"][0]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <base-map-svg
              bronhouderType="Waterschap"
              headerVariable="waterschappen"
              geojsonFile="waterschapsgrenzen.json"
              overlayMode="objecttypen"
              v-if="model && 'static' in model"
              :staticContent="model.static"
              :dataTypen="model.static_data['data_waterschap_typen']"
              :dataRegimes="model.static_data['data_waterschap_regimes']"
            />
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-separator class="divider" />
      <h2>En verder</h2>
      <q-expansion-item id="expansion-item-top-20" v-model="top20Expanded">
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="top20Expanded.toString()"
            aria-label="Open"
          >
            <q-icon name="table_view" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Top-20</h3>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['top20-registratieobjecten']"
            ></div>
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item id="expansion-item-trends" v-model="trendsExpanded">
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="trendsExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="timeline" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Trends</h3>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
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

            <div
              v-if="model && 'static' in model && model.static[optionSelected]"
              v-html="model.static[optionSelected]"
            ></div>
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item id="expansion-item-stand" v-model="standExpanded">
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="standExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="bar_chart" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Stand</h3>
          </q-item-section>
          <q-item-section side>
            <b>
              {{
                model &&
                "static_data" in model &&
                model.static_data["totaal_aantal_objecten"]
              }}
            </b>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['registratieobjecten-staaf']"
            ></div>
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        id="expansion-item-trends"
        v-model="actualiteitExpanded"
      >
        <template v-slot:header>
          <q-item-section
            avatar
            role="button"
            :aria-expanded="actualiteitExpanded.toString()"
            aria-label="Open"
          >
            <q-icon name="source" color="primary" size="24px" />
          </q-item-section>
          <q-item-section>
            <h3>Actualiteit van de gegevens</h3>
          </q-item-section>
        </template>
        <q-card>
          <q-card-section>
            <div
              v-if="model && 'static' in model"
              v-html="model.static['actualiteit']"
            ></div>
            <br />
          </q-card-section>
          <hr role="presentation" />
        </q-card>
      </q-expansion-item>
      <div class="row justify-center">
        <img
          style="width: 48px !important"
          alt="BRO Logo"
          :src="require('@/assets/bro_logo.png')"
        />
      </div>
    </div>
    <div
      v-if="
        loaded &&
        model &&
        'static_data' in model &&
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
          v-if="model && 'html' in model"
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

import {
  documentTypeLegendData,
  qualityRegimeLegendData,
} from "@/utils/legendData";
import LegendTable from "@/components/LegendTable.vue";
import BaseMapSvg from "@/views/reports/bronhoudermaps/BaseMapSvg.vue";
import { BromonitorModel, BromonitorModelRecent } from "@/models/aggregate";
import { defineComponent } from "vue";

export default defineComponent({
  components: {
    LegendTable,
    BaseMapSvg,
  },
  data() {
    const dateOptions = {
      timeZone: "Europe/Amsterdam",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const loaded = false;
    // const model: BromonitorModel | BromonitorModelRecent | null = null;
    // const dates = [];
    // const selectedDate = null;
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
    // Separate v-models for each accordeon to manage aria-expanded labelling.
    const actieveBronhoudersExpanded = false;
    const aantalRegistratiesExpanded = false;
    const gldExpanded = false;
    const gemeentenExpanded = false;
    const provinciesExpanded = false;
    const waterschappenExpanded = false;
    const top20Expanded = false;
    const trendsExpanded = false;
    const standExpanded = false;
    const actualiteitExpanded = false;
    return {
      dateOptions,
      dates: [] as string[],
      selectedDate: null as string | null,
      loaded,
      model: null as BromonitorModel | BromonitorModelRecent | null,
      objectLegendData,
      regimeLegendData,
      optionSelected,
      trendOptions,
      scTimer,
      scY,
      actieveBronhoudersExpanded,
      aantalRegistratiesExpanded,
      gldExpanded,
      gemeentenExpanded,
      provinciesExpanded,
      waterschappenExpanded,
      top20Expanded,
      trendsExpanded,
      standExpanded,
      actualiteitExpanded,
    };
  },
  props: {
    date: String,
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
      return window.location.href.includes(this.$data.selectedDate || "");
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
        this.$data.dates = (await getBromonitorDates()).dates.map((date) =>
          new Date(date).toISOString(),
        );
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
    date: function () {
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
#archive-monitor :deep(.assistive-button) {
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

.red-text {
  color: red !important;
}
</style>
