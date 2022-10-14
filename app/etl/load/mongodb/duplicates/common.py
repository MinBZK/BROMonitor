from .cpt import cpt_duplicates_by_bronhouder, cpt_duplicates_by_location


def duplicates_by_location(db):
    """
    Creates a materialized view containing duplicates of all regristration types based on location.
    Results are grouped by location and type.
    CPT subresults use a more specific algorithm.
    """
    db.duplicatesByLocation.drop()
    # Duplicate algorithm for non CPT objects
    db.common.aggregate([
        {
            "$sort": {"common.deliveredLocation.pos": 1}
        },
        {
            "$match": {"common.type": {"$ne": "GeotechnischSondeeronderzoek"}}
        },
        {
            "$match": {"common.deliveredLocation.pos": {"$ne": None}}
        },
        {
            "$group": {
                "_id": {"location": "$common.deliveredLocation.pos",
                        "type": "$common.type"},
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

    # Specific algorithm for cpts
    cpt_duplicates_by_location(db)


def duplicates_by_bronhouder(db):
    """
    Creates a materialized view containing duplicates of all regristration types from a bronhouder point of view.
    Results are grouped by location and type.
    CPT subresults use a more specific algorithm.
    """
    db.duplicatesByBronhouder.drop()
    # Duplicate algorithm for non CPT objects
    db.common.aggregate([
        {
            "$sort": {"common.deliveredLocation.pos": 1}
        },
        {
            "$match": {"common.type": {"$ne": "GeotechnischSondeeronderzoek"}}
        },
        {
            "$match": {"common.deliveredLocation.pos": {"$ne": None}}
        },
        {
            "$group": {
                "_id": {
                    "location": "$common.deliveredLocation.pos",
                    "type": "$common.type"},
                "count": {"$sum": 1},
                "bronhouders": {
                    "$addToSet": "$common.deliveryAccountableParty"},
                "objects": {
                    "$addToSet": {
                        "type": "$common.type",
                        "broid": "$common.broId",
                        "kvk": "$common.deliveryAccountableParty"}}
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

    # Specific algorithm for cpts
    cpt_duplicates_by_bronhouder(db)
