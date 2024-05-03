from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gmn(classes):

    class GMN_Measuring_Point_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmn_measuringpoint"]
            load_instance = True
            # list of GMW_Tube objects
            include_relationships = True
            exclude = ["gm_gmn_measuringpoint_pk"]

    class GMN_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmn"]
            load_instance = True
            exclude = ["gm_gmn_pk"]
        # Overwrite the generated measuringpoints to a nested one-to-many
        # list of measuringpoint objects
        gm_gmn_measuringpoint_collection = Nested(
            GMN_Measuring_Point_Schema, many=True)

    return GMN_Schema()
