import logging
from .duplicates.common import duplicates_by_bronhouder, duplicates_by_location


def update_materialized_views(db):
    log = logging.getLogger(__name__)
    log.info(
        """Creating materialized view for the count
        of CPT per year per IMBRO/IMBRO A""")
    count_cpt_per_year(db)
    log.info("Creating materialized view for the duplicates by location")
    duplicates_by_location(db)
    log.info(
        "Creating materialized view for the document counts by bronhouder")
    document_counts_by_bronhouder(db)
    log.info(
        "Creating materialized view for the duplicates by bronhouder")
    duplicates_by_bronhouder(db)
    log.info(
        """Creating materialized view for the count
        of GLD per bronhouder""")
    gld_counts_by_bronhouder(db)


def count_cpt_per_year(db):
    db.CPToverTime.drop()
    db.specificCPT.aggregate([
        {
            "$group": {
                "_id": {
                    "jaar": {
                        "$cond": {
                            "if":
                            {"$gt":
                             [{"$strLenCP":
                               "$conePenetrometerSurvey.conePenetrationTest.startTime"},
                              4]},
                            "then":
                            {"$toString":
                             {"$year": {"$dateFromString": {
                                 "dateString":
                                 "$conePenetrometerSurvey.conePenetrationTest.startTime",
                                 "onError": "$NULL"}}}},
                            "else":
                            {"$toString":
                             "$conePenetrometerSurvey.conePenetrationTest.startTime"}
                        }
                    },
                    "kwaliteit": "$qualityRegime"
                },
                "count": {"$sum": 1}
            }
        },
        {"$merge": {"into": {"db": "bro", "coll": "CPToverTime"},
                    "on": "_id",
                    "whenMatched": "replace", "whenNotMatched": "insert"}}
    ])


def document_counts_by_bronhouder(db):
    db.documentCountsByBronhouder.drop()
    db.common.aggregate([
        {
            "$sort": {"common.deliveryAccountableParty": 1, "common.type": 1}
        },
        {
            "$group": {
                "_id": {"kvk": "$common.deliveryAccountableParty",
                        "type": "$common.type"},
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id.kvk": -1, "count": -1}
        },
        {"$merge": {"into":
                    {"db": "bro", "coll": "documentCountsByBronhouder"},
                    "on": "_id", "whenMatched": "replace",
                    "whenNotMatched": "insert"}}
    ])


def gld_counts_by_bronhouder(db):
    db.gldsCountsByBronhouder.drop()
    db.specificGLD.aggregate([
        {
            "$project": {
                "deliveryAccountableParty": 1,
                "registrationHistory.registrationStatus": 1
            }
        },
        {
            "$group": {
                "_id": {
                    "kvk": "$deliveryAccountableParty",
                    "type": "Grondwaterstandonderzoek",
                    "status": "$registrationHistory.registrationStatus"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {"$merge": {"into":
                    {"db": "bro", "coll": "gldsCountsByBronhouder"},
                    "on": "_id", "whenMatched": "replace",
                    "whenNotMatched": "insert"}}
    ])
