from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gmn(classes):

    # class GMN_Registration_History_Schema(CamelCaseSchema):
    #     class Meta:
    #         model = classes["registration_history"]
    #         load_instance = True

    class GMN_Groundwater_Monitoring_Tube_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmw_monitoringtube"]
            load_instance = True
            exclude = ["gm_gmw_monitoringtube_pk"]

    class GMN_Measuring_Point_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmn_measuringpoint"]
            load_instance = True
            exclude = ["gm_gmn_measuringpoint_pk"]
        gm_gmw_monitoringtube_collection = Nested(
            GMN_Groundwater_Monitoring_Tube_Schema, many=True)

    class GMN_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gmn"]
            load_instance = True
            exclude = ["standardized_location",
                       "gm_gmn_pk"]
        # registration_history_collection = Nested(
        #     GMN_Registration_History_Schema, many=True)
        gm_gmn_measuringpoint_collection = Nested(
            GMN_Measuring_Point_Schema, many=True)

    return GMN_Schema()
