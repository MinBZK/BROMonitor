from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_bhrp(classes):

    class BHR_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True
            include_relationships = False

    class BHR_Delivered_Location_Schema(CamelCaseSchema):
        class Meta:
            model = classes["delivered_location"]
            load_instance = True
            include_relationships = False

    class BHR_Schema(CamelCaseSchema):
        class Meta:
            model = classes["borehole_research"]
            include_relationships = False
            load_instance = True
            exclude = ["standardized_location"]
        delivered_location_collection = Nested(
            BHR_Delivered_Location_Schema, many=True)
        registration_history_collection = Nested(
            BHR_Registration_History_Schema, many=True)

    return BHR_Schema()
