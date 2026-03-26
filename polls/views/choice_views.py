from rest_framework import viewsets, status
from rest_framework.response import Response
from polls.services.choice_service import ChoiceService
from rest_framework.permissions import IsAuthenticated

class ChoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        choices = ChoiceService.list_choices_for_question(question_pk)
        return Response(choices)

    def create(self, request, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = ChoiceService.create_choice(request.user, question_pk, choice_text)
        return Response(choice, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = ChoiceService.update_choice(request.user, pk, choice_text)
        return Response(choice)

    def retrieve(self, request, pk=None, question_pk=None):
        choice = ChoiceService.get_choice(pk)
        return Response(choice)

    def destroy(self, request, pk=None, question_pk=None):
        ChoiceService.delete_choice(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
