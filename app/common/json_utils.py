import xmltodict

namespaces = {
    "http://www.opengis.net/gml/3.2": None,
    "http://www.opengis.net/swe/2.0": None,
    "http://www.opengis.net/om/2.0": None,
    "http://www.opengis.net/sampling/2.0": None,
    "http://www.w3.org/2001/XMLSchema-instance": None,
    "http://www.w3.org/1999/xlink": None,
    "http://www.pdok.nl/bro": None,
    "http://www.broservices.nl/xsd/brocommon/3.0": None,
    "http://www.broservices.nl/xsd/bhrcommon/1.1": None,
    "http://www.broservices.nl/xsd/cptcommon/1.1": None,
    "http://www.broservices.nl/xsd/gmwcommon/1.1": None,
    "http://www.broservices.nl/xsd/dsbhr/1.1": None,
    "http://www.broservices.nl/xsd/dscpt/1.1": None,
    "http://www.broservices.nl/xsd/dsgmw/1.1": None
}


def xml_to_json(xml):
    return xmltodict.parse(xml, process_namespaces=True, namespaces=namespaces)


def json_to_document_type(json):
    return json["common"]["type"]
