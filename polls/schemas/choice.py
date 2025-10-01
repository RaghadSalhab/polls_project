# schemas/choice.py
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from polls.models.choice import Choice
from .base import BaseSchema

class ChoiceSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Choice

    id = auto_field()
    choice_text = auto_field()
    votes = auto_field()
    question = Nested("QuestionSchema", only=("id", "question_text"))
