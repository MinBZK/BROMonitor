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
    db.specificCPT.aggregate([
        {
            "$group": {
                "_id": CPT_DUPLICATE_CRITERIAS,
                "count": {"$sum": 1},
                "bronhouders": {
                    "$addToSet": "$deliveryAccountableParty"},
                "objects": {
                    "$addToSet": {
                        "type": "GeotechnischSondeeronderzoek",
                        "broid": "$broId",
                        "kvk": "$deliveryAccountableParty"}}
            }
        },
        {
            "$match": {"count": {"$gt": 1}}
        },
        {"$merge": {"into": {"db": "bro", "coll": "duplicatesByBronhouder"},
                    "on": "_id",
                    "whenMatched": "replace",
                    "whenNotMatched": "insert"}
         }
    ], allowDiskUse=True)
