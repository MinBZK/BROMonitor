import Vue from "vue";

import "quasar/dist/quasar.min.css";
import "quasar/dist/quasar.addon.min.css";
import lang from "./quasar-lang-nl";
import "@quasar/extras/material-icons/material-icons.css";
import {
  Quasar,
  QBanner,
  QBreadcrumbs,
  QBreadcrumbsEl,
  QBtn,
  QBtnDropdown,
  QCard,
  QCardSection,
  QDrawer,
  QExpansionItem,
  QFooter,
  QIcon,
  QHeader,
  QInnerLoading,
  QInput,
  QItem,
  QItemSection,
  QItemLabel,
  QLayout,
  QList,
  QPageContainer,
  QPage,
  QPageSticky,
  QRadio,
  QRouteTab,
  QSelect,
  QSeparator,
  QSlideTransition,
  QSpace,
  QSpinner,
  QTab,
  QTable,
  QTabs,
  QTabPanels,
  QTabPanel,
  QToggle,
  QTh,
  QTr,
  QTd,
  QToolbar,
  QToolbarTitle,
} from "quasar";

// Dynamically switch branding based on the base url of the application.
// Normally header and footer are RO blauw.
const brand = {
  primary: "#01689b",
  secondary: "#01689b",
  tertiary: "#b3d2e1",
  accent: "#a90061",

  positive: "#39870c",
  negative: "#d52b1e",
  info: "#8fcae7",
  warning: "#ffb612",

  bodyFontSize: "18px",
  inputFontSize: "18px",

  typographyFontFamily:
    "'RO Sans', '-apple-system', 'Helvetica Neue', Helvetica, Arial, sans-serif",
};

// Switch to purple as secondary colour for acceptation environment.
if (window.location.host.startsWith("acc.")) {
  brand["secondary"] = "#42145f";
}

Vue.use(Quasar, {
  config: {
    brand: brand,
  },
  components: {
    QBanner,
    QBreadcrumbs,
    QBreadcrumbsEl,
    QBtn,
    QBtnDropdown,
    QCard,
    QCardSection,
    QDrawer,
    QExpansionItem,
    QFooter,
    QIcon,
    QHeader,
    QInnerLoading,
    QInput,
    QItem,
    QItemSection,
    QItemLabel,
    QLayout,
    QList,
    QPageContainer,
    QPage,
    QPageSticky,
    QRadio,
    QRouteTab,
    QSelect,
    QSeparator,
    QSlideTransition,
    QSpace,
    QSpinner,
    QTab,
    QTabPanels,
    QTabPanel,
    QTable,
    QTabs,
    QToggle,
    QTh,
    QTr,
    QTd,
    QToolbar,
    QToolbarTitle,
  },
  directives: {},
  plugins: {},
  lang: lang,
});
