<template>
  <div>
    <spinner :loaded="loaded" />
    <div>
      <h3 class="sr-only">
        {{ header }}
      </h3>
      <div class="row">
        <div class="col-xs-12 col-lg-6">
          <div class="column">
            <p>{{ text }}</p>
            <div class="overlay-toolbar">
              <input type="radio" :id="'objecttypen' + bronhouderType" :name="'overlay-' + bronhouderType"
                value="objecttypen" v-model="currentMode" checked />
              <label :aria-label="bronhouderType + ' kaart toont objecttypen.'"
                :for="'objecttypen' + bronhouderType">Objecttypen</label>
              <input type="radio" :id="'kwaliteitsregimes' + bronhouderType" :name="'overlay-' + bronhouderType"
                value="kwaliteitsregimes" v-model="currentMode" />
              <label :aria-label="bronhouderType + ' kaart toont kwaliteitsregimes.'"
                :for="'kwaliteitsregimes' + bronhouderType">Kwaliteitsregimes</label>
            </div>
            <br />
            <legend-table v-show="loaded" :data="legendData"
              :legendId="currentMode + '-' + bronhouderType + '-legenda'" />
          </div>
          <br />
        </div>
        <div class="col-xs-12 col-lg-6" v-show="loaded">
          <div class="q-py-md">
            <div class="map-skiplink">
              <a :href="currentMode == 'objecttypen'
                ? '#button-table-types-' + bronhouderType.toLowerCase()
                : '#button-table-kwaliteitsregimes-' +
                bronhouderType.toLowerCase()
                " style="color: #ffffff">
                Spring focus over de kaart heen
              </a>
            </div>
          </div>
          <div class="svg-container">
            <svg :id="'bronhoudermap-' + bronhouderType"></svg>
            <div class="tooltip-container" :id="'ttcontainer-' + bronhouderType" style="display: none"
              aria-hidden="true"></div>
          </div>
        </div>
      </div>
      <button class="button-table assistive-button" :id="currentMode == 'objecttypen'
        ? 'button-table-types-' + bronhouderType.toLowerCase()
        : 'button-table-kwaliteitsregimes-' + bronhouderType.toLowerCase()
        " :alt="'Tabel met aantal registraties per' + bronhouderType.toLowerCase()
          " ref="toonDataTabel">
        Toon datatabel
      </button>
      <div v-if="staticContent" v-html="staticContent[tblKey]"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { brondocumentCountPerBronhouder } from "@/services/aggregates";
// import { DataModel } from "@/models/aggregate";
// import { ref } from "vue";
import {
  PerBronhouderCountAggregate,
  QualityRegimeAggregate,
  BronhouderDocumentCount,
} from "@/models/aggregate";
import LegendTable from "@/components/LegendTable.vue";
import {
  documentTypeLegendData,
  qualityRegimeLegendData,
} from "@/utils/legendData";
import * as d3 from "d3";
import { defineComponent } from "vue";
import content from "@/content.json";
import { useI18n } from "vue-i18n";
import { useAnnouncer } from "@vue-a11y/announcer";

interface ContentMap {
  [key: string]: {
    header: string;
    text: string;
  };
}

export default defineComponent({
  components: {
    LegendTable,
  },
  data() {
    const loaded = false;
    const defaultMode = "objecttypen";
    const currentMode = "";
    const legendData = documentTypeLegendData;
    content;
    const header = "";
    const text = "";
    const tblKey = "";
    return {
      loaded,
      defaultMode,
      currentMode,
      legendData,
      content,
      header,
      text,
      tblKey,
    };
  },
  props: {
    bronhouderType: {
      type: String,
      default: "",
    },
    headerVariable: String,
    geojsonFile: {
      type: String,
      default: "",
    },
    overlayMode: String,
    staticContent: Object,
    dataTypen: Array,
    dataRegimes: Array,
  },
  watch: {
    currentMode: function (newVal) {
      this.$data.header = this.getHeader();
      this.$data.text = this.getText();
      this.clearSvg();
      this.createMap(
        newVal,
        this.$props.geojsonFile,
        this.$props.bronhouderType,
      );
      this.$data.tblKey = this.getTableKey();
      if (newVal == "objecttypen") {
        this.$data.legendData = documentTypeLegendData;
      } else {
        this.$data.legendData = qualityRegimeLegendData;
      }
      this.resetTableDataButton();
    },
  },
  methods: {
    initToolTip(): d3.Selection {
      return d3
        .select("#ttcontainer-" + this.bronhouderType)
        .append("div")
        .attr("class", "tooltip");
    },
    initSvg(): d3.Selection {
      return d3
        .select("#bronhoudermap-" + this.bronhouderType)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "100 0 720  800")
        .classed("svg-content-responsive", true)
        .attr(
          "aria-label",
          this.bronhouderType + " kaart " + this.$data.currentMode,
        );
    },
    initPath(data): d3.geoPath {
      const projection = d3
        .geoIdentity()
        .reflectY(true)
        .fitSize([800, 700], data);
      return d3.geoPath(projection);
    },
    clearSvg() {
      d3.select("#bronhoudermap-" + this.bronhouderType)
        .selectAll("*")
        .remove();
      d3.select("#ttcontainer-" + this.bronhouderType)
        .selectAll(".tooltip")
        .remove();
    },
    tooltipHandler(d: d3, tooltip: d3.Selection): void {
      let htmlString = d.target.__data__.properties.bronhouder + "</br><hr>";
      const classificationString = this.getClassificationString(
        d.target.__data__.properties.tooltips,
      );
      //let announcerString =
      //  d.target.__data__.properties.bronhouder + ". " + classificationString;
      htmlString += classificationString + "</br></br>";

      if (d.target.__data__.properties.tooltips != undefined) {
        d.target.__data__.properties.tooltips.sort().forEach((x) => {
          htmlString += x.key + ": " + this.n(x.count) + "</br>";
        });
      }
      // if (d.target.__data__.properties.tooltips != undefined) {
      //  d.target.__data__.properties.tooltips.sort().forEach((x) => {
      //   announcerString += x.key + " " + this.n(x.count) + ". ";
      //  });
      // }
      tooltip
        .html(htmlString)
        .style("left", 0 + "px")
        .style("top", 0 + "px")
        .attr("aria-live", "assertive");
      const x = document.getElementById("ttcontainer-" + this.bronhouderType)!;
      x.style.display = "block";
      //this.polite(announcerString);
    },
    getClassificationString(data) {
      const dataobject = {};
      data.forEach((x) => {
        dataobject[x.key] = x.count;
      });
      if (this.currentMode === "objecttypen") {
        if (dataobject["GLD met watermetingen"] > 0) {
          return "Heeft één of meerdere grondwaterstandmetingen geregistreerd. ";
        } else if (dataobject["CPT"] > 0 || dataobject["GMW"] > 0 || dataobject["GAR"] > 0 || dataobject["GUF"] > 0 || dataobject["GPD"] > 0 || dataobject["BHR-GT"] > 0) {
          return "Heeft één of meerdere gegevens geregistreerd. ";
        } else {
          return "Heeft geen gegevens geregistreerd. ";
        }
      } else {
        if (Object.prototype.hasOwnProperty.call(dataobject, "IMBRO")) {
          return "Heeft één of meerdere objecten in kwaliteitsregime IMBRO geregistreerd. ";
        } else if (
          Object.prototype.hasOwnProperty.call(dataobject, "IMBRO/A")
        ) {
          return "Heeft enkel objecten in kwaliteitsregime IMBRO/A geregistreerd. ";
        } else {
          return "Heeft geen objecten geregistreerd. ";
        }
      }
    },
    objectTypeOverlay(
      d: d3,
      bronhouderData: BronhouderDocumentCount[],
    ): string {
      const code = d.properties.statcode;
      const dataObject = bronhouderData.find((x) => x.identifier == code);
      if (dataObject != null) {
        d.properties.bronhouder = dataObject.naam;
        d.properties.tooltips = [
          { key: "CPT", count: dataObject.cpt },
          { key: "GMW", count: dataObject.gmw },
          { key: "GLD", count: dataObject.gld },
          { key: "GLD met watermetingen", count: dataObject.gldAangevuld },
          { key: "GAR", count: dataObject.gar },
          { key: "GUF", count: dataObject.guf },
          { key: "GPD", count: dataObject.gpd },
          { key: "BHR-GT", count: dataObject.bhrgt },
        ];
        if (dataObject.gldAangevuld > 0) {
          return "rgba(85, 177, 165,  1)";
        } else if (dataObject.cpt > 0 || dataObject.gmw > 0 || dataObject.gar > 0 || dataObject.guf > 0 || dataObject.gpd > 0 || dataObject.bhrgt > 0) {
          return "rgba(237, 208, 136, 1)";
        }
      }
      return "rgba(199, 81, 70, 1)";
    },
    qualityRegimeOverlay(
      d: d3,
      bronhouderData: QualityRegimeAggregate[],
    ): string {
      const code = d.properties.statcode;
      const dataObject = bronhouderData.find((x) => x.identifier == code);
      if (dataObject != null) {
        d.properties.bronhouder = dataObject.bronhouder;
        d.properties.tooltips = dataObject.quality_regimes;
        if (dataObject.quality_regimes.map((x) => x.key).includes("IMBRO")) {
          return "rgba(85, 177, 165, 1)";
        } else if (
          dataObject.quality_regimes.map((x) => x.key).includes("IMBRO/A")
        ) {
          return "rgba(237, 208, 136, 1)";
        }
      }
      return "rgba(199, 81, 70, 1)";
    },
    createMap(
      overlay: string,
      jsonInput: string,
      bronhouderType: string,
    ): void {
      this.$data.loaded = false;
      // const localmodel = ref<DataModel>({});
      let bronhouderData;
      let overlayHandler;
      const fetchData = async (): Promise<void> => {
        // Fetch the correct data, pick the correct overlay handler
        if (overlay == "objecttypen") {
          bronhouderData = brondocumentCountPerBronhouder(
            this.$props.dataTypen as PerBronhouderCountAggregate[],
          );
          overlayHandler = this.objectTypeOverlay;
        } else if (overlay == "kwaliteitsregimes") {
          bronhouderData = this.$props.dataRegimes as QualityRegimeAggregate[];
          overlayHandler = this.qualityRegimeOverlay;
        }
        // Create base map of the Netherlands+bronhouders
        const data = require("@/utils/geojson/" + jsonInput);
        const tooltip = this.initToolTip();
        const svg = this.initSvg();
        const path = this.initPath(data);
        // Create overlay and eventhandlers
        svg
          .selectAll("path")
          .data(data.features)
          .enter()
          .append("path")
          .attr("id", (d) => {
            return bronhouderType + "-" + d.properties.statnaam;
          })
          .attr("d", path)
          .attr("stroke", "black")
          .join("path")
          .attr("fill", (d) => {
            return overlayHandler(d, bronhouderData);
          })
          .on("mousemove touchstart focus", (d) => {
            this.tooltipHandler(d, tooltip);
          })
          .on("mouseout touchend focusout", function () {
            const x = document.getElementById("ttcontainer-" + bronhouderType)!;
            x.style.display = "none";
          });
        this.$data.loaded = true;
      };
      fetchData();
    },
    getHeader(): string {
      return (content.map as ContentMap)[this.$data.currentMode].header.replace(
        "BRONHOUDERTYPE",
        this.$props.headerVariable ?? "",
      );
    },
    getText(): string {
      return (content.map as ContentMap)[this.$data.currentMode].text.replace(
        "BRONHOUDERTYPE",
        this.$props.bronhouderType.toLowerCase(),
      );
    },
    getTableKey(): string {
      if (this.$data.currentMode == "objecttypen") {
        return "table-types-" + this.$props.bronhouderType.toLowerCase();
      } else {
        return (
          "table-kwaliteitsregimes-" + this.$props.bronhouderType.toLowerCase()
        );
      }
    },
    resetTableDataButton() {
      const button = this.$refs["toonDataTabel"] as HTMLElement;
      button.innerHTML = "Toon datatabel";
    },
  },
  mounted() {
    this.$data.currentMode = this.$props.overlayMode || "";
    this.$data.header = this.getHeader();
    this.$data.text = this.getText();
    this.$data.tblKey = this.getTableKey();
  },
  setup() {
    const { n } = useI18n();
    const { polite } = useAnnouncer();
    return {
      n,
      polite,
    };
  },
});
</script>
<style scoped>
svg {
  padding-left: 10%;
}

.svg-content-responsive {
  display: inline-block;
  position: absolute;
  top: 10px;
  left: 0;
  box-sizing: initial;
}

.svg-content-responsive :deep(path:active),
.svg-content-responsive :deep(path:focus),
.svg-content-responsive :deep(path:hover) {
  outline: none;
  stroke-width: 3 !important;
}

.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  vertical-align: top;
}

.tooltip-container :deep(.tooltip) {
  background-color: white;
  border: 1px solid #cccccc;
  font-size: 1rem;
  padding: 15px;
  pointer-events: none;
  position: absolute;
  max-width: 33%;
}

:deep(.tooltip) {
  hyphens: auto;
  word-break: break-word;
}

.map-skiplink {
  z-index: 100;
  width: 100%;
  height: 44px;
  position: relative;
}

.map-skiplink>a {
  background-color: #01689b;
  border: none;
  border-radius: 0;
  color: #fff;
  cursor: pointer;
  font-size: 1.26562rem;
  line-height: 1.58025;
  min-height: 44px;
  padding: 0.75rem 1rem;
  text-decoration: none !important;
  width: auto;
  position: absolute;
  left: -100vw;
  top: -100vh;
}

.map-skiplink>a:focus {
  -webkit-box-shadow: 0 0 0 2px #fff;
  box-shadow: 0 0 0 2px #fff;
  outline: 2px dotted #000;
  outline-offset: 0;
  z-index: 1010;
  left: 15px;
  top: 15px;
}

.map-skiplink>a:hover {
  background-color: #01496d;
  color: #fff;
}

.map-skiplink>a:visited {
  color: white;
}
</style>
