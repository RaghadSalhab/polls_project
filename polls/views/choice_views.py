from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from polls.services.choice_service import ChoiceService
from polls.serializers import QuestionSerializer, ChoiceSerializer
from polls.utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ChoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        choices = ChoiceService.list_choices_for_question(question_pk)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def create(self, request, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = ChoiceService.create_choice(request.user,question_pk, choice_text)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, question_pk=None):
        choice_text = request.data.get("choice_text")
        user = request.user
        choice = ChoiceService.update_choice(user, pk, choice_text)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None,question_pk=None):
        choice = ChoiceService.get_choice(pk)
        if not choice:
            return Response({"choice": "Not found"}, status=404)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    def destroy(self, request, pk=None, question_pk=None):
        ChoiceService.delete_choice(request.user,pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
