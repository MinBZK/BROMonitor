import {
  BromonitorModel,
  BromonitorModelRecent,
  DatesModel
} from "@/models/aggregate";
import { http } from "@/utils/request";

const ENDPOINT = "/bromonitor";

export const getBromonitorDates = (): Promise<DatesModel> =>
  http({
    url: `${ENDPOINT}/bromonitor-datums`,
    method: "get"
  }).then(response => response.data);

export const getBromonitor = (DATUM: string): Promise<BromonitorModel> =>
  http({
    url: `${ENDPOINT}/bromonitor`,
    method: "get",
    params: {
      datum: DATUM
    }
  }).then(response => response.data);

export const getBromonitorRecent = (): Promise<BromonitorModelRecent> =>
  http({
    url: `${ENDPOINT}/bromonitor-recent`,
    method: "get"
  }).then(response => response.data);

export const getBromonitorEmbedded = (): Promise<BromonitorModel> =>
  http({
    url: `${ENDPOINT}/bromonitor-embedded`,
    method: "get"
  }).then(response => response.data);
