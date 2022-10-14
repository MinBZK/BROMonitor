<template>
  <q-table
    class="col-12"
    :data="tableData"
    :columns="tableColumns"
    :row-key="rowKey ? rowKey : rowKeyLambda ? rowKeyLambda : {}"
    separator="horizontal"
    :filter="filter"
    :filter-method="filterMethod"
    dense
    flat
    binary-state-sort
    color="primary"
    v-on="rowClickHandler ? { 'row-click': rowClickHandler } : {}"
    ref="bmTable"
  >
    <template v-slot:top-left v-if="downloadable">
      <q-btn
        class="assistive-button btn-download"
        label="Download CSV"
        no-caps
        flat
        @click="download(tableData, tableColumns)"
        aria-label="Download CSV"
      />
    </template>
    <template v-slot:top-right v-if="searchable">
      <q-input
        borderless
        dense
        debounce="300"
        v-model="filter"
        aria-label="Zoekveld"
        placeholder="Zoeken binnen tabel"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template v-slot:bottom="scope">
      <span aria-hidden="true">Records per pagina:&nbsp;</span>
      <q-select
        v-model="scope.pagination.rowsPerPage"
        borderless
        options-dense
        :aria-label="`records per pagina: ${scope.pagination.rowsPerPage}`"
        :options="[5, 10, 15, 20, 25, 50, 0]"
        :option-label="item => (item === 0 ? 'Alle' : item)"
      />
      <span>
        {{
          (
            (scope.pagination.page - 1) * scope.pagination.rowsPerPage +
            1
          ).toLocaleString("nl-NL")
        }}
        -
        {{
          Math.min(
            scope.pagination.page * scope.pagination.rowsPerPage,
            filter ? filteredRowCount : tableData.length
          ).toLocaleString("nl-NL")
        }}
        van
        {{
          filter
            ? filteredRowCount.toLocaleString("nl-NL")
            : tableData.length.toLocaleString("nl-NL")
        }}
      </span>
      <q-btn
        v-if="scope.pagesNumber > 2"
        icon="first_page"
        color="primary"
        round
        dense
        flat
        :disable="scope.isFirstPage"
        @click="scope.firstPage"
        aria-label="Ga naar eerste pagina"
      ></q-btn>

      <q-btn
        icon="chevron_left"
        color="primary"
        round
        dense
        flat
        :disable="scope.isFirstPage"
        @click="scope.prevPage"
        aria-label="Ga naar vorige pagina"
      ></q-btn>

      <q-btn
        icon="chevron_right"
        color="primary"
        round
        dense
        flat
        :disable="scope.isLastPage"
        @click="scope.nextPage"
        aria-label="Ga naar volgende pagina"
      ></q-btn>
      <q-btn
        v-if="scope.pagesNumber > 2"
        icon="last_page"
        color="primary"
        round
        dense
        flat
        :disable="scope.isLastPage"
        @click="scope.lastPage"
        aria-label="Ga naar laatste pagina"
      ></q-btn>
    </template>
    <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
  </q-table>
</template>

<script lang="ts">
import Vue from "vue";
import { downloadTable } from "@/services/downloadService";

export default Vue.extend({
  data() {
    const filter = "";
    const pagination = {};
    const filteredRowCount = 0;
    return { filter, pagination, filteredRowCount };
  },
  props: {
    tableData: Array,
    tableColumns: Array,
    tableFilter: String,
    rowKey: String,
    rowKeyLambda: Function,
    downloadable: { default: true, type: Boolean },
    downloadFileName: { default: "table-export", type: String },
    searchable: { default: true, type: Boolean },
    rowClickHandler: Function
  },
  watch: {
    tableFilter: function(newVal, oldVal) {
      this.initiateFilter();
    }
  },
  methods: {
    download(data: any, columns: any) {
      downloadTable(
        (this.$refs.bmTable as any).filteredSortedRows,
        columns,
        this.$props.downloadFileName
      );
    },
    initiateFilter() {
      this.$data.filter = this.$props.tableFilter;
    },
    filterMethod(rows, terms) {
      // Checks if any of the columns of a row contain the filtered term.
      const lowerTerms = terms ? terms.toLowerCase() : "";
      const columns = this.$props.tableColumns.map(x => x.field);
      const filteredRows = rows.filter(row =>
        columns.some(col => (row[col] + "").toLowerCase().includes(lowerTerms))
      );
      this.$data.filteredRowCount = filteredRows.length;
      return filteredRows;
    }
  },
  beforeMount() {
    if (this.$props.tableFilter) {
      this.initiateFilter();
    }
  }
});
</script>
