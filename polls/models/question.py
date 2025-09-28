from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', default=1)

    def __str__(self):
        return self.question_text

    class Meta:
        app_label = 'polls'
