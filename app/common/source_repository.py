import os
from pymongo import MongoClient
from common.source import Source
from dateutil import parser

class SourceRepository(object):

    def __init__(self):
        mongoUrl = os.environ.get('mongodbUrl')
        client = MongoClient(mongoUrl)
        self.db = client.bro

    def _update_field(self, doc_type, field, value):
        self.db.source.update_one({"type": doc_type}, 
                {"$set": {field: value}}, upsert=True)

    def set_updated(self, doc_type, updated):
        self._update_field(doc_type, 'updated', updated)

    def set_last_queried(self, doc_type,last_extracted):
        self._update_field(doc_type, "last_queried", last_extracted)

    def set_last_loaded(self, doc_type, last_loaded):
        self._update_field(doc_type, "last_loaded", last_loaded)

    def set_zip_filename(self, doc_type, zip_filename):
        self._update_field(doc_type, "zip_filename", zip_filename)

    def set_status(self, doc_type, status):
        self._update_field(doc_type, 'status', status)

    def insert_source(self, doc_type, name, status = "OK", zip_filename = "" ):
        return self.db.source.insert_one({
            "type": doc_type,
            "name": name,
            "status": status,
            "updated": parser.parse('2021-01-01T00:00:00.000+00:00'),
            "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
            "last_loaded" : parser.parse('2021-01-01T00:00:00.000+00:00'),
            "zip_filename": zip_filename })

    def remove(self, doc_type):
        self.db.source.delete_one({'type': doc_type})

    def all(self):
        return self.db.source.find({})
    
    def count(self):
        return self.db.source.count_documents({})

    def get_by_type(self, doc_type):
        return self.db.source.find_one({'type': doc_type })

    def get_status(self, doc_type):
        doc = self.db.source.find_one({'type': doc_type })
        return doc['status']

    def get_latest_date_of_source(self, name):
        self.db.source.find({'name': name}).sort({'last_loaded': -1}).limit(1)

