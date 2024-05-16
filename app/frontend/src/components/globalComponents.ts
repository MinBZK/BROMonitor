// Declare components in this file that are re-used on multiple pages in the application.
// This way the component is declared globally and doesn't have to be included separately on each page.
import Spinner from "@/components/loadingIndicators/Spinner.vue";
import Timestamp from "@/components/texts/Timestamp.vue";
import Textbox from "@/components/texts/Textbox.vue";
import PageTitle from "@/components/texts/PageTitle.vue";
import PageSubtitle from "@/components/texts/PageSubtitle.vue";

// Declare the global components using "Vue.component(name to use in templates, name of vue component)"
export function GlobalComponents(app) {
  app.component("spinner", Spinner);
  app.component("timestamp", Timestamp);
  app.component("textbox", Textbox);
  app.component("page-title", PageTitle);
  app.component("page-subtitle", PageSubtitle);
}
