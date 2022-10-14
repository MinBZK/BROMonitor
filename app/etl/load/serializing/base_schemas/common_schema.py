from marshmallow import Schema, fields
from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema


class Common_Schema(CamelCaseSchema):
    bro_id = fields.Str(dump_only=True)
    delivery_accountable_party = fields.Str(dump_only=True)
    quality_regime = fields.Str(dump_only=True)
    x_or_lon = fields.Str(dump_only=True)
    y_or_lat = fields.Str(dump_only=True)
    object_registration_time = fields.Str(dump_only=True)
