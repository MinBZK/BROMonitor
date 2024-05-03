from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from etl.load.serializing.base_schemas.camel_case_schema import CamelCaseSchema
from etl.load.serializing.base_schemas.common_schema import Common_Schema


def serializer_cpt(classes):
    class CPT_Registration_History_Schema(CamelCaseSchema):
        class Meta:
            model = classes["registration_history"]
            load_instance = True
            include_relationships = False

    class CPT_Cone_Penetration_Test(CamelCaseSchema):
        class Meta:
            model = classes["cone_penetration_test"]
            # include_relationships = True
            include_fk = True
            load_instance = True

    class CPT_Cone_Penetrometer_Survey(CamelCaseSchema):
        class Meta:
            model = classes["cone_penetrometer_survey"]
            include_relationships = True
            include_fk = True
            load_instance = True
        cone_penetration_test_collection = Nested(
            CPT_Cone_Penetration_Test, many=True)

    class CPT_Schema(CamelCaseSchema):
        class Meta:
            model = classes["geotechnical_cpt_survey"]
            include_relationships = True
            load_instance = True
        cone_penetrometer_survey_collection = Nested(
            CPT_Cone_Penetrometer_Survey, many=True)
        registration_history_collection = Nested(
            CPT_Registration_History_Schema, many=True)

    return CPT_Schema()
