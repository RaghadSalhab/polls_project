from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validates_schema, ValidationError
from polls.models.user import User
from .base import BaseSchema

class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User

    id = auto_field()
    username = auto_field()
    email = auto_field()
    password = auto_field(load_only=True)
    password2 = fields.String(load_only=True) 

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get("password") != data.get("password2"):
            raise ValidationError("Passwords must match.", field_name="password2")
