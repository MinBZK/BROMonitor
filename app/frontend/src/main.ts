import Default from "@/layouts/Default.vue";
import Embeddable from "@/layouts/Embeddable.vue";
import { Layout } from "@/layouts/layout";
import VueCompositionApi from "@vue/composition-api";
import Vue, { ComponentOptions } from "vue";
import VueI18n from "vue-i18n";
import App from "./App.vue";
import store from "@/utils/store";
import axios from "axios";
import router from "./router";
import "./quasar";
import "@/components/globalComponents.ts";
import { UpdateHTTPSettings } from "@/utils/request";
import VueAnnouncer from "@vue-a11y/announcer";

Vue.config.productionTip = false;
Vue.use(VueCompositionApi);
Vue.use(VueI18n);
Vue.use(VueAnnouncer, { complementRoute: "is geladen" }, router);

export const i18n = new VueI18n({
  locale: "nl",
  fallbackLocale: "nl",
  messages: {},
});

// Register the different layouts used.
Vue.component(Layout.Default, Default as ComponentOptions<any>);
Vue.component(Layout.Embeddable, Embeddable as ComponentOptions<any>);

// Loading initial settings and localization files before building the Vue instance.
axios
  .get(window.location.origin + "/settings.json") // Store settings
  .then((response) => {
    store.settings = response.data;
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
    i18n.setLocaleMessage("nl", messages.data);
    i18n.locale = "nl";
    new Vue({
      router,
      i18n,
      render: (h) => h(App),
    }).$mount("#app");
  });
