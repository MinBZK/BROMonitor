import { http } from "@/utils/request";
import { CountAggregate } from "@/models/aggregate";

const ENDPOINT = "/pagevisits";

export const logPageVisit = (PATH: string) =>
  http({
    url: `${ENDPOINT}/log-page-visit`,
    method: "get",
    params: {
      url: PATH,
    },
  });

export const getPageVisits = (DAGEN: number): Promise<CountAggregate[]> =>
  http({
    url: `${ENDPOINT}/gebruiksstatistieken`,
    method: "get",
    params: {
      dagen: DAGEN,
    },
  }).then((response) => response.data);
