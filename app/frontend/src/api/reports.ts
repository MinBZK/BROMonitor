import { DataModel } from "@/models/aggregate";
import { http } from "@/utils/request";

const ENDPOINT = "/rapporten";

export const getBrondocumentenPerBronhouder = (): Promise<DataModel> =>
  http({
    url: `${ENDPOINT}/brondocumenten-per-bronhouder`,
    method: "get"
  }).then(response => response.data);

export const getBrondocumentenPerBronhouderVanType = (
  BRONHOUDERTYPE: string,
  GLD: string,
  ONLY_BRONHOUDERS: boolean = false
): Promise<DataModel> =>
  http({
    url: `${ENDPOINT}/brondocumenten-per-bronhouder`,
    method: "get",
    params: {
      bronhoudertype: BRONHOUDERTYPE,
      gldstatus: GLD,
      only_bronhouders: ONLY_BRONHOUDERS
    }
  }).then(response => response.data);

export const getKwaliteitsregimesPerBronhouderVanType = (
  BRONHOUDERTYPE: string
): Promise<DataModel> =>
  http({
    url: `${ENDPOINT}/kwaliteitsregimes-per-bronhouder`,
    method: "get",
    params: {
      bronhoudertype: BRONHOUDERTYPE
    }
  }).then(response => response.data);

export const getDocumentTypes = (): Promise<DataModel> =>
  http({
    url: `${ENDPOINT}/documenttypes`,
    method: "get"
  }).then(response => response.data);
