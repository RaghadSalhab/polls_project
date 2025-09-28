from django.contrib import admin
from polls.models.choice import Choice
from polls.models.question import Question
admin.site.register(Choice)
admin.site.register(Question)
# Register your models here.
