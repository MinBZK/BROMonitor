from backend.models.documenttype import DocumentType

registration_type_dict = {
    "BHR": "BHR_REGISTRATION_V11",
    "CPT": "CPT_REGISTRATION_V11",
    "GMW": "GMW_REGISTRATION_V11"
}

DOCUMENT_TYPES = [
    DocumentType(shortName='BHR-P',
                 longName='Bodemkundig booronderzoek',
                 dbName='BodemkundigBooronderzoek',
                 domain='Bodem-en grondonderzoek',
                 defaultGraph=""),
    DocumentType(shortName='CPT',
                 longName='Geotechnisch sondeeronderzoek',
                 dbName='GeotechnischSondeeronderzoek',
                 domain='Bodem-en grondonderzoek',
                 defaultGraph="cptCombinedLength"),
    DocumentType(shortName='GMW',
                 longName='Grondwatermonitoringput',
                 dbName='Grondwatermonitoringput',
                 domain='Grondwatermonitoring',
                 defaultGraph="simpleWellDisplay"),
    DocumentType(shortName='SFR',
                 longName='Bodemkundig wandonderzoek',
                 dbName='BodemkundigWandonderzoek',
                 domain='Bodem-en grondonderzoek',
                 defaultGraph=""),
    DocumentType(shortName='BHR-GT',
                 longName='Geotechnisch booronderzoek',
                 dbName='GeotechnischBooronderzoek',
                 domain='Bodem-en grondonderzoek',
                 defaultGraph=""),
    DocumentType(shortName='GMN',
                 longName='Grondwatermonitoringnet',
                 dbName='Grondwatermonitoringnet',
                 domain='Grondwatermonitoring',
                 defaultGraph="",
                 typeHasLocation=False),
    DocumentType(shortName='GLD',
                 longName='Grondwaterstandonderzoek',
                 dbName='Grondwaterstandonderzoek',
                 domain='Grondwatermonitoring',
                 defaultGraph="",
                 typeHasLocation=False)
]


class DocumentTypeRegistry():
    def __init__(self, document_types):
        self.document_types = document_types

    def get_types(self):
        return self.document_types

    def get_short_names(self):
        return list(map(lambda d: d.shortName, self.document_types))

    def get_short_by_longname(self, longName):
        return next((d.shortName for d in self.document_types if d.longName == longName), None)

    def _get_type_by_dbname(self, dbname):
        return next((d for d in self.document_types if d.dbName == dbname), None)

    def get_short_by_dbname(self, dbname):
        return self._get_type_by_dbname(dbname).shortName

    def get_long_by_dbname(self, dbname):
        return self._get_type_by_dbname(dbname).longName


document_type_registry = DocumentTypeRegistry(DOCUMENT_TYPES)
