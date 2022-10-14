import { DocumentType } from "@/models/documentType";
import { Bronhouder } from "@/models/bronhouder";

const store = {
  // Will receive our config.json file content
  settings: { vueAppBaseApi: "http://localhost:8000/api", timeoutTime: 10 },
  documentTypes: [],
  bronhouders: [],
  pageStates: {},
};

export default store;

export function getTypesWithLocations() {
  return (store.documentTypes as DocumentType[]).filter(
    (t) => t.typeHasLocation
  );
}

export function getTypeByDbName(dbName) {
  return store.documentTypes.find((x: DocumentType) => x.dbName == dbName);
}

export function getTypeByLongName(longName) {
  return store.documentTypes.find((x: DocumentType) => x.longName == longName);
}

export function getTypeByShortName(shortName) {
  return store.documentTypes.find(
    (x: DocumentType) => x.shortName == shortName
  );
}

export function getBronhouderByKvK(kvk) {
  const bronhouder = store.bronhouders.find((x: Bronhouder) => x.kvk == kvk);
  if (bronhouder) {
    return bronhouder;
  } else {
    return { kvk: kvk, name: `Bronhouder met KvK ${kvk}` } as Bronhouder;
  }
}

export function getPageState(identifier) {
  return store.pageStates[identifier];
}

export function setPageState(identifier, payload) {
  store.pageStates[identifier] = payload;
}
