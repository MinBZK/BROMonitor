import {
  BronhouderDocumentCount,
  PerBronhouderCountAggregate,
} from "@/models/aggregate";

interface DocumentCount {
  naam?: string;
  identifier?: string;
  cpt: number;
  gmw: number;
  bhrp: number;
  sfr: number;
  bhrgt: number;
  gmn: number;
  gld: number;
  gldAangevuld: number;
}

export function brondocumentCountPerBronhouder(
  data: PerBronhouderCountAggregate[]
): BronhouderDocumentCount[] {
  const aggregate: { [kvk: string]: DocumentCount } = data.reduce((agg, e) => {
    const r =
      agg[e.key.kvk] ||
      ({
        cpt: 0,
        gmw: 0,
        bhrp: 0,
        sfr: 0,
        bhrgt: 0,
        gmn: 0,
        gld: 0,
        gldAangevuld: 0,
        naam: e.key.naam,
        identifier: e.key.identifier,
      } as DocumentCount);

    if (e.key.type === "GeotechnischSondeeronderzoek") {
      r.cpt = e.count;
    } else if (e.key.type === "Grondwatermonitoringput") {
      r.gmw = e.count;
    } else if (e.key.type === "BodemkundigBooronderzoek") {
      r.bhrp = e.count;
    } else if (e.key.type === "BodemkundigWandonderzoek") {
      r.sfr = e.count;
    } else if (e.key.type === "GeotechnischBooronderzoek") {
      r.bhrgt = e.count;
    } else if (e.key.type === "Grondwatermonitoringnet") {
      r.gmn = e.count;
    } else if (e.key.type === "Grondwaterstandonderzoek") {
      r.gld = e.count;
    } else if (e.key.type === "Grondwaterstandonderzoek_aangevuld") {
      r.gldAangevuld = e.count;
    }

    agg[e.key.kvk] = r;
    return agg;
  }, {} as { [kvk: string]: DocumentCount });

  return Object.keys(aggregate).map(
    (k) =>
      ({
        kvk: k,
        naam: aggregate[k].naam,
        identifier: aggregate[k].identifier,
        cpt: aggregate[k].cpt,
        gmw: aggregate[k].gmw,
        bhrp: aggregate[k].bhrp,
        sfr: aggregate[k].sfr,
        bhrgt: aggregate[k].bhrgt,
        gmn: aggregate[k].gmn,
        gld: aggregate[k].gld,
        gldAangevuld: aggregate[k].gldAangevuld,
      } as BronhouderDocumentCount)
  );
}
