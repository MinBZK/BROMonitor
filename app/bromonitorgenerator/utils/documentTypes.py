import requests
import json

from bromonitorgenerator.utils.utils import API_BASE

document_type_dict = dict()
short_to_dutch_fullname = dict()


def init_document_registries():
    response = requests.get(API_BASE + "/metadata/documenttypes")
    data = json.loads(response.content)
    for d in data:
        dbName = d.get('dbName')
        shortName = d.get('shortName')
        longName = d.get('longName')

        document_type_dict[dbName] = shortName
        short_to_dutch_fullname[shortName] = longName
