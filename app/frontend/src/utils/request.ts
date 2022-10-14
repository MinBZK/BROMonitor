import axios from "axios";
import store from "@/utils/store";

export let http = axios.create({
  baseURL: store.settings.vueAppBaseApi,
  timeout: store.settings.timeoutTime
});
export function UpdateHTTPSettings() {
  http = axios.create({
    baseURL: store.settings.vueAppBaseApi,
    timeout: store.settings.timeoutTime
  });
}