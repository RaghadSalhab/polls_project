# # schemas/question.py
# from marshmallow_sqlalchemy import auto_field
# from marshmallow_sqlalchemy.fields import Nested
# from polls.models.question import Question
# from .base import BaseSchema

# class QuestionSchema(BaseSchema):
#     class Meta(BaseSchema.Meta):
#         model = Question

#     id = auto_field()
#     question_text = auto_field()
#     pub_date = auto_field()
#     created_by = Nested("UserSchema", only=("id", "username"))
#     choices = Nested("ChoiceSchema", many=True, exclude=("question",))
# schemas/question.py
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from polls.models.question import Question
from .base import BaseSchema

from .user import UserSchema      # <-- استيراد UserSchema مباشرة
from .choice import ChoiceSchema  # <-- استيراد ChoiceSchema مباشرة

class QuestionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Question

    id = auto_field()
    question_text = auto_field()
    pub_date = auto_field()
    created_by = Nested(UserSchema, only=("id", "username"))   # <-- استخدمي class مباشرة
    choices = Nested(ChoiceSchema, many=True, exclude=("question",))  # <-- نفس الشي
