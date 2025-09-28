from polls.models.choice import Choice
from django.core.exceptions import ObjectDoesNotExist
from polls.models.question import Question

    # ----------- Choices -----------
class ChoiceRepository:

    @staticmethod
    def list_choices_for_question(question_id):
        return Choice.objects.filter(question_id=question_id)

    @staticmethod
    def get_choice(choice_id):
        try:
            return Choice.objects.select_related('question').get(id=choice_id)
        except Choice.DoesNotExist:
            return None

    @staticmethod
    def create_choice(question_id, choice_text):
        question = Question.objects.get(id=question_id)
        return Choice.objects.create(question=question, choice_text=choice_text)

    @staticmethod
    def update_choice(choice_id, choice_text):
        choice = Choice.objects.get(id=choice_id)
        choice.choice_text = choice_text
        choice.save()
        return choice

    @staticmethod
    def delete_choice(choice_id):
        Choice.objects.filter(id=choice_id).delete()

    # ----------- Voting -----------

    @staticmethod
    def vote(choice_id):
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()
        return choice
