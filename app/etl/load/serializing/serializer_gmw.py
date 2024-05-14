from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gmw(classes):

    class GMW_Tube_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmw_monitoringtube"]
            load_instance = True
            exclude = ["gm_gmw_monitoringtube_pk"]

    class GMW_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmw"]
            load_instance = True
            exclude = ["gm_gmw_pk"]
        # Overwrite the generated monitoring tubes to a nested one-to-many
        # list of GMW_Tube objects
        gm_gmw_monitoringtube_collection = Nested(
            GMW_Tube_Schema, many=True)

    return GMW_Schema()
