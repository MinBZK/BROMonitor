<template>
  <q-page>
    <spinner :loaded="loaded" />
    <div class="row" v-show="loaded">
      <page-title :text="$t('analyse_1.titel')" />
      <textbox :text="$t('analyse_1.uitleg')" />
      <bm-table
        :tableData="countData"
        :tableColumns="columns"
        :tableFilter="bronhouder"
        row-key="kvk"
      />
    </div>
  </q-page>
</template>

<script lang="ts">
import { getBrondocumentenPerBronhouder } from "@/api/reports";
import { getPaginationByField } from "@/utils/tableUtils/pagination";
import {
  DataModel,
  PerBronhouderCountAggregate,
  BronhouderDocumentCount,
} from "@/models/aggregate";
import { brondocumentCountPerBronhouder } from "@/services/aggregates";
import { downloadTable } from "@/services/downloadService";
import { ref } from "vue";
import { defineComponent } from "vue";
import BmTable from "@/components/BmTable.vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
  components: {
    BmTable,
  },
  data() {
    const columns = [
      {
        name: "bronhouder",
        label: "Bronhouder",
        field: "naam",
        align: "left",
        sortable: true,
        classes: "ellipsis",
      },
      {
        name: "kvk",
        label: "KvK-nummer",
        field: "kvk",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
      },
      {
        name: "cpt",
        label: "CPT's",
        field: "cpt",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "gmn",
        label: "GMN's",
        field: "gmn",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "gmw",
        label: "GMW's",
        field: "gmw",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "gld",
        label: "GLD's",
        field: "gld",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "bhrp",
        label: "BHR-P's",
        field: "bhrp",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "bhrgt",
        label: "BHR-GT's",
        field: "bhrgt",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
      {
        name: "sfr",
        label: "SFR's",
        field: "sfr",
        align: "left",
        style: "max-width: 120px",
        sortable: true,
        classes: "ellipsis",
        format: (val: number) => this.n(val),
      },
    ];
    const filter = "";
    return { columns, filter };
  },
  methods: {
    download(data: unknown, columns: unknown) {
      downloadTable(data, columns);
    },
  },
  props: {
    bronhouder: String,
  },
  setup() {
    const model = ref<DataModel>({
      data: [],
      sources: [],
    });
    const countData = ref<BronhouderDocumentCount[]>([]);
    const loaded = ref<boolean>(false);
    const pagination = getPaginationByField("cpt", true);
    const fetchData = async (): Promise<void> => {
      model.value = await getBrondocumentenPerBronhouder();
      countData.value = brondocumentCountPerBronhouder(
        model.value.data as PerBronhouderCountAggregate[],
      );
      loaded.value = true;
    };
    const { n } = useI18n();

    fetchData();

    return {
      model,
      countData,
      pagination,
      loaded,
      n,
    };
  },
});
</script>
