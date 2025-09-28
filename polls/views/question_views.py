# polls/views/question_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from polls.services.poll_service import PollService
from polls.serializers import QuestionSerializer, ChoiceSerializer
from polls.utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class QuestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        search = request.query_params.get("search")
        questions = PollService.list_questions(search)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        question = PollService.get_question(pk)
        if not question:
            return Response({"detail": "Not found"}, status=404)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def create(self, request):
        user = request.user
        question_text = request.data.get("question_text")
        choices = request.data.get("choices", [])

        question = PollService.create_question(user, question_text, choices)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        question_text = request.data.get("question_text")
        choices = request.data.get("choices") 
        user = request.user
        question = PollService.update_question(user, pk, question_text, choices)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        PollService.delete_question(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        choice_id = request.data.get("choice_id")
        choice = PollService.vote(choice_id)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)


class ChoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        choices = PollService.list_choices_for_question(question_pk)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def create(self, request, question_pk=None):
        choice_text = request.data.get("choice_text")
        choice = PollService.create_choice(request.user,question_pk, choice_text)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, question_pk=None):
        choice_text = request.data.get("choice_text")
        user = request.user
        choice = PollService.update_choice(user, pk, choice_text)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None,question_pk=None):
        choice = PollService.get_choice(pk)
        if not choice:
            return Response({"choice": "Not found"}, status=404)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    def destroy(self, request, pk=None, question_pk=None):
        PollService.delete_choice(request.user,pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
