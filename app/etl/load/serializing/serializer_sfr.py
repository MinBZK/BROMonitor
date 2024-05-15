from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_sfr(classes):

    class SFR_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True

    class SFR_Delivered_Location_Schema(CamelCaseSchema):
        class Meta:
            model = classes["delivered_location"]
            load_instance = True

    class SFR_Schema(CamelCaseSchema):
        class Meta:
            model = classes["soil_face_research"]
            include_relationships = True
            load_instance = True
            exclude = ["standardized_location"]
        delivered_location_collection = Nested(
            SFR_Delivered_Location_Schema, many=True)
        registration_history_collection = Nested(
            SFR_Registration_History_Schema, many=True)

    return SFR_Schema()
