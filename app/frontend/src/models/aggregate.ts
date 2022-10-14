import { SourceModel } from "@/models/source";

export interface DataModel {
  data: Aggregate[];
  sources: SourceModel[];
}

export interface DatesModel {
  dates: Date[];
}

// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Aggregate {}

export interface BromonitorModel extends Aggregate {
  date: string;
  html: string;
}

export interface BromonitorModelRecent extends BromonitorModel {
  static: Object;
  static_data: Object;
}

export interface CountAggregate extends Aggregate {
  key: string;
  count: number;
}

export interface QualifiedCountAggregate extends CountAggregate {
  domain: string;
  qualifiedName: string;
}

export interface PerBronhouderCountAggregate extends Aggregate {
  key: BronhouderAndType;
  count: number;
}

export interface BronhouderAndType extends Aggregate {
  kvk: string;
  naam?: string;
  identifier?: string;
  status?: string;
  type: string;
}

export interface BronhouderDocumentCount extends Aggregate {
  kvk: string;
  naam?: string;
  identifier?: string;
  cpt: number;
  gmw: number;
  bhrp: number;
  sfr: number;
  gmn: number;
  gld: number;
  gldAangevuld: number;
}

export interface QualityRegimeAggregate extends Aggregate {
  bronhouder: string;
  identifier?: string;
  quality_regimes: CountAggregate[];
}

interface MapContent {
  bronhouderType: string;
  headerVariabele: string;
  geojsonFile: string;
  staticContent: string;
  dataTypen: string;
  dataRegimes: string;
  className?: string;
}


export interface BroMonitorItemModel {
  id: string;
  iconName: string;
  title: string;
  sectionSideValue: string;
  contentSelectors?: string[];
  mapContent?: MapContent;
}
