from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gmw(classes):
    class GMW_Electrode_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gmw_electrode"]
            include_fk = True
            load_instance = True

    class GMW_Geo_Ohm_Cable_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gmw_geo_ohm_cable"]
            include_relationships = True
            include_fk = True
            load_instance = True
        # Overwrite the generated electrodes to a nested one-to-many list
        # of GMW_Electrode objects
        gmw_electrode_collection = Nested(GMW_Electrode_Schema, many=True)

    class GMW_Tube_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gmw_monitoring_tube"]
            include_relationships = True
            include_fk = True
            load_instance = True
        # Overwrite the generated geo ohm cables to a nested one-to-many list
        # of GMW_Geo_Ohm_Cable objects
        gmw_geo_ohm_cable_collection = Nested(
            GMW_Geo_Ohm_Cable_Schema, many=True)

    class GMW_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gmw_monitoring_well"]
            include_relationships = True
            load_instance = True
            exclude = ["standardized_location"]
        # Overwrite the generated monitoring tubes to a nested one-to-many
        # list of GMW_Tube objects
        gmw_monitoring_tube_collection = Nested(GMW_Tube_Schema, many=True)

    return GMW_Schema()
