from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_bhrgt(classes):
    class BHRGT_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True
            include_relationships = False

    class BHRGT_Boring_Schema(CamelCaseSchema):
        class Meta:
            model = classes["boring"]
            load_instance = True
            include_relationships = False

    class BHRGT_Delivered_Location_Schema(CamelCaseSchema):
        class Meta:
            model = classes["delivered_location"]
            load_instance = True
            include_relationships = False

    class BHRGT_Schema(CamelCaseSchema):
        class Meta:
            model = classes["borehole_research"]
            include_relationships = False
            load_instance = True
            exclude = ["standardized_location"]
        boring_collection = Nested(
            BHRGT_Boring_Schema, many=True)
        delivered_location_collection = Nested(
            BHRGT_Delivered_Location_Schema, many=True)
        registration_history_collection = Nested(
            BHRGT_Registration_History_Schema, many=True)

    return BHRGT_Schema()
