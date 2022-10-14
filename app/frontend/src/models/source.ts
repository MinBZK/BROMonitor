export interface SourceModel{
    name: string;
    types: SourceTypeModel[];
  }

export interface SourceTypeModel{
    type: string;
    updated: Date;
}