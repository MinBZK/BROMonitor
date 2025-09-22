from collections import defaultdict


# Fields to be use in the group phase of the aggregation of duplicates
CPT_DUPLICATE_CRITERIAS = {"location": {"$concat": ["$xOrLon", " ", "$yOrLat"]},
                           "type": "GeotechnischSondeeronderzoek",
                           "finalDepth":  "$conePenetrometerSurvey.finalDepth"}


def cpt_duplicates_by_location(db):
    """
    Algorithm to determine CPT duplicates per location.
    This method adds a check on "finalDepth" in addition to the standard location+type check.
    """
    db.specificCPT.aggregate([
        {
            "$group": {
                "_id": CPT_DUPLICATE_CRITERIAS,
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {"count": {"$gt": 1}}
        },
        {
            "$sort": {"count": -1}
        },
        {"$merge": {"into": {"db": "bro", "coll": "duplicatesByLocation"},
                    "on": "_id",
                    "whenMatched": "replace",
                    "whenNotMatched": "insert"}}
    ], allowDiskUse=True)


def cpt_duplicates_by_bronhouder(db):
    """
    Algorithm to determine CPT duplicates per bronhouder.
    This method adds a check on "finalDepth" in addition to the standard location+type check.
    """
    documents = db.specificCPT.find()

    groups = defaultdict(list)
    for doc in documents:
        if all(field in doc for field in CPT_DUPLICATE_CRITERIAS):
            key = tuple(doc[field] for field in CPT_DUPLICATE_CRITERIAS)
            groups[key].append(doc)

    for key, docs in groups.items():
        if len(docs) > 1:
            result = {
                "_id": key,
                "count": len(docs),
                "bronhouders": list({doc["deliveryAccountableParty"] for doc in docs}),
                "objects": [{
                    "type": "GeotechnischSondeeronderzoek",
                    "broid": doc["broId"],
                    "kvk": doc["deliveryAccountableParty"]
                } for doc in docs]
            }
 
            db.bro.duplicatesByBronhouder.replace_one({"_id": result["_id"]}, result, upsert=True)
