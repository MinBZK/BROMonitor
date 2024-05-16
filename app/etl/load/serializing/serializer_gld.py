from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_gld(classes):

    class GLD_Schema(CamelCaseSchema):
        class Meta:
            model = classes["gm_gld"]
            load_instance = True
            exclude = ["gm_gld_pk"]

    return GLD_Schema()
