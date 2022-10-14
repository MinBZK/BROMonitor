from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Transforms a string from snake case to camel case


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)

# Extend the Base schema to transform all the output keys to camelcase
# instead of snake case


class CamelCaseSchema(SQLAlchemyAutoSchema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
