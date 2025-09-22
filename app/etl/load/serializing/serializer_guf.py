from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema

def serializer_guf(classes):

    class GUF_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True
            include_relationships = False
        
    class GUF_Schema(CamelCaseSchema):
        class Meta:
            model = classes["groundwater_usage_facility"]
            include_relationships = False
            load_instance = True
            exclude = ['standardized_location']
        registration_history_collection = Nested(
            GUF_Registration_History_Schema, many=True)
        
    return GUF_Schema()