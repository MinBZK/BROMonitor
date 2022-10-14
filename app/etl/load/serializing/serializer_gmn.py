from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gmn(classes):

    class GMN_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True

    class GMN_Groundwater_Monitoring_Tube_Schema(CamelCaseSchema):
        class Meta:
            model = classes["groundwater_monitoring_tube"]
            load_instance = True
            exclude = ["groundwater_monitoring_tube_pk"]

    class GMN_Measuring_Point_With_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["measuring_point_with_history"]
            load_instance = True
            exclude = ["measuring_point_with_history_pk"]
        groundwater_monitoring_tube_collection = Nested(
            GMN_Groundwater_Monitoring_Tube_Schema, many=True)

    class GMN_Schema(CamelCaseSchema):
        class Meta:
            model = classes["groundwater_monitoring_net"]
            load_instance = True
            exclude = ["standardized_location",
                       "groundwater_monitoring_net_pk"]
        registration_history_collection = Nested(
            GMN_Registration_History_Schema, many=True)
        measuring_point_with_history_collection = Nested(
            GMN_Measuring_Point_With_History_Schema, many=True)

    return GMN_Schema()
