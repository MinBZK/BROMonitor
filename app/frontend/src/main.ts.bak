import Default from "@/layouts/Default.vue";
import Embeddable from "@/layouts/Embeddable.vue";
import { Layout } from "@/layouts/layout";
import { ComponentOptions } from "vue";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import { createApp } from "vue";
import store from "@/utils/store";
import axios from "axios";
import router from "./router";
import "./quasar";
import "@/components/globalComponents";
import { UpdateHTTPSettings } from "@/utils/request";
import VueAnnouncer from "@vue-a11y/announcer";
import { GlobalComponents } from "@/components/globalComponents";
import { Quasar } from "quasar";
import { quasarOptions } from "./quasar";

const i18n = createI18n({
  legacy: false,
  locale: "nl",
  fallbackLocale: "nl",
  messages: {},
});

export const app = createApp(App);
app.use(Quasar, quasarOptions);
app.use(i18n);
app.use(VueAnnouncer);
GlobalComponents(app);

// Register the different layouts used.
app.component(
  Layout.Default,
  Default as ComponentOptions<Record<string, never>>,
);
app.component(
  Layout.Embeddable,
  Embeddable as ComponentOptions<Record<string, never>>,
);

// Loading initial settings and localization files before building the Vue instance.
axios
  .get(window.location.origin + "/settings.json") // Store settings
  .then((response) => {
    store.settings.vueAppBaseApi = response.data.vueAppBaseApi;
    store.settings.timeoutTime = response.data.timeoutTime;
    UpdateHTTPSettings();
    return axios.get(store.settings.vueAppBaseApi + "/metadata/documenttypes"); // Store documenttypes
  })
  .then((response) => {
    store.documentTypes = response.data;
    return axios.get(store.settings.vueAppBaseApi + "/rapporten/bronhouders"); // Bronhouders
  })
  .then((response) => {
    store.bronhouders = response.data;
    return axios.get(store.settings.vueAppBaseApi + "/i18n/nl-NL"); // Store i18n
  })
  .then((messages) => {
    i18n.global.setLocaleMessage("nl", messages.data);
    i18n.global.locale.value = "nl";
    app.use(router);
    app.mount("#app");
  });
