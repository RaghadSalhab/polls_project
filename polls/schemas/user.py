# schemas/user.py
from marshmallow_sqlalchemy import auto_field
from polls.models.user import User
from .base import BaseSchema

class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User

    id = auto_field()
    username = auto_field()
    email = auto_field()
    password = auto_field(load_only=True)
