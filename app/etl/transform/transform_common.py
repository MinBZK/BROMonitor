import json
from pyproj import Transformer

transformer = Transformer.from_crs("epsg:28992", "epsg:4326")

# Transforms the common section of a Geopackage based object.
# - Transforms xOrLon and yOrLat to deliverred location
# - Adds the geojson object to the json document
# - Adds the full type name to the document
# - Encapsulates the document in a "common" object.


def transform_common(json_input, type):
    if "xOrLon" in json_input and "yOrLat" in json_input:
        x1 = json_input["xOrLon"]
        y1 = json_input["yOrLat"]
        x2, y2 = transformer.transform(x1, y1)

        json_input["geojson"] = {
            "type": "Point",
            "coordinates": [x2, y2]
        }

        json_input["deliveredLocation"] = {
            "crs": "urn:ogc:def:crs:EPSG::28992",
            "pos": x1 + " " + y1
        }
        json_input.pop("xOrLon")
        json_input.pop("yOrLat")

    json_input["type"] = type
    json_input = {"common": json_input}
    return json_input
