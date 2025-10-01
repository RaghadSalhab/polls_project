# schemas/question.py
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from polls.models.question import Question
from .base import BaseSchema

class QuestionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Question

    id = auto_field()
    question_text = auto_field()
    pub_date = auto_field()
    created_by = Nested("UserSchema", only=("id", "username"))
    choices = Nested("ChoiceSchema", many=True, exclude=("question",))
