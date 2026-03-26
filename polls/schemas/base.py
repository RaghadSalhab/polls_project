# schemas/base.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from polls.models.database import Session

class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        sqla_session = Session
