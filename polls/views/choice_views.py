from rest_framework import viewsets, status
from rest_framework.response import Response
from polls.services.choice_service import ChoiceService
from polls.schemas.choice import ChoiceSchema 
from rest_framework.permissions import IsAuthenticated
from polls.models.database import Session  

class ChoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        choices = ChoiceService.list_choices_for_question(question_pk)
        schema = ChoiceSchema(many=True)
        data = schema.dump(choices)
        return Response(data)

    def create(self, request, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = ChoiceService.create_choice(request.user, question_pk, choice_text)
        schema = ChoiceSchema()
        data = schema.dump(choice)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = ChoiceService.update_choice(request.user, pk, choice_text)
        schema = ChoiceSchema()
        data = schema.dump(choice)
        return Response(data)

    def retrieve(self, request, pk=None, question_pk=None):
        choice = ChoiceService.get_choice(pk)
        schema = ChoiceSchema()
        data = schema.dump(choice)
        return Response(data)

    def destroy(self, request, pk=None, question_pk=None):
        ChoiceService.delete_choice(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
