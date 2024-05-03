import BroMonitor from "@/views/BroMonitor.vue";
import BroMonitorArchive from "@/views/BroMonitorArchive.vue";
import BrondocumentenPerBronhouder from "@/views/reports/BrondocumentenPerBronhouder.vue";
import Markdown from "@/components/Markdown.vue";
import PageVisits from "@/views/PageVisits.vue";
import NotFound from "@/views/NotFound.vue";
import Sitemap from "@/views/Sitemap.vue";
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import qs from "qs";
import { logPageVisit } from "@/api/pageVisits";

const routes: Array<RouteRecordRaw> = [
  {
    path: "",
    name: "bro-monitor",
    component: BroMonitor,
    meta: { breadCrumb: "sectie_1.broodkruimel" },
    props: (route) => ({ date: route.query.datum }),
  },
  {
    path: "/inbedbaar/monitor",
    name: "monitor-embeddable",
    meta: {
      layout: "embeddable",
    },
    component: BroMonitor,
  },
  {
    path: "/archief",
    name: "bro-monitor-archive",
    component: BroMonitorArchive,
    meta: { breadCrumb: "bromonitor_archief.broodkruimel" },
  },
  {
    path: "/cookies-en-privacy",
    name: "cookies_privacy",
    component: Markdown,
    props: { data: require("@/assets/markdown/cookies_privacy.md") },
  },
  {
    path: "/kwetsbaarheid-melden",
    name: "kwetsbaarheid-melden",
    component: Markdown,
    props: {
      data: require("@/assets/markdown/Kwetsbaarheid melden.md"),
    },
  },
  {
    path: "/over-de-bro-monitor",
    name: "overdebromonitor",
    component: Markdown,
    props: {
      data: require("@/assets/markdown/informatie.md"),
    },
  },
  {
    path: "/toegankelijkheid",
    name: "toegankelijkheid",
    component: Markdown,
    props: {
      data: require("@/assets/markdown/Toegankelijkheid.md"),
    },
  },
  {
    path: "/download-gegevens-per-bronhouder",
    name: "gegevens-per-bronhouder",
    component: BrondocumentenPerBronhouder,
    meta: { breadCrumb: "analyse_1.broodkruimel" },
    props: (route) => ({ bronhouder: route.query.bronhouder }),
  },
  {
    path: "/gebruiksstatistieken",
    name: "page-visits",
    component: PageVisits,
    meta: { breadCrumb: "Gebruiksstatistieken" },
  },
  {
    path: "/niet-gevonden",
    name: "not-found",
    meta: { breadCrumb: "Niet gevonden" },
    component: NotFound,
  },
  {
    path: "/:catchAll(.*)",
    name: "catch-all",
    component: NotFound,
  },
  {
    path: "/sitemap",
    name: "sitemap",
    component: Sitemap,
    meta: { breadCrumb: "Sitemap" },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  stringifyQuery: (query) => {
    const result = qs.stringify(query, { format: "RFC1738" });
    return result ? "?" + result : "";
  },
  routes,
});

// Sets the tabtitle by the most specific part of the route.
router.beforeEach((to, from, next) => {
  let path = to.path;
  logPageVisit(path);
  path = to.path.split("/").slice(-1)[0];
  path = path.split("-").join(" ");
  path = path
    .toLowerCase()
    .split(" ")
    .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
    .join(" ");
  let title = "BRO Monitor";
  if (path) {
    title += ` | ${path}`;
  }
  document.title = title;
  next();
});

export default router;
