from backend.models.documenttype import DocumentType
from backend.utils.documentTypes import DocumentTypeRegistry

TEST_DOCUMENT_TYPES = [
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
EXPECTED_SHORTNAMES = ['BHR-P', "CPT", "GMW", "GMN", "GLD"]


def test_document_type_registry():
    document_type_registry = DocumentTypeRegistry(TEST_DOCUMENT_TYPES)
    # Test if the types of the registry are the same as the expected types
    assert document_type_registry.get_types() == TEST_DOCUMENT_TYPES
    # Test if the shortnames are the same as the expect shortnames
    assert EXPECTED_SHORTNAMES == document_type_registry.get_short_names()
