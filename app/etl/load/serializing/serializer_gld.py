from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gld(classes):

    # class GMN_Registration_History_Schema(CamelCaseSchema):
    #     class Meta:
    #         model = classes["registration_history"]
    #         load_instance = True

    class GLD_Groundwater_Monitoring_Tube_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmw_monitoringtube"]
            load_instance = True
            exclude = ["gm_gmw_monitoringtube_pk"]

    class GLD_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gld"]
            load_instance = True
            exclude = ["standardized_location",
                       "gm_gld_pk"]
        gm_gmw_monitoringtube_collection = Nested(
            GLD_Groundwater_Monitoring_Tube_Schema, many=True)

    return GLD_Schema()
