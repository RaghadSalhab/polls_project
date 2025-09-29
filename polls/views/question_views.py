from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from polls.services.question_service import QuestionService
from polls.services.choice_service import ChoiceService
from polls.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.permissions import IsAuthenticated

class QuestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        search = request.query_params.get("search")
        questions = QuestionService.list_questions(request.db, search)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        question = QuestionService.get_question(request.db, pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def create(self, request):
        user = request.user
        question_text = request.data.get("question_text")
        choices = request.data.get("choices", [])

        question = QuestionService.create_question(request.db, user, question_text, choices)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        question_text = request.data.get("question_text")
        choices = request.data.get("choices")
        user = request.user

        question = QuestionService.update_question(request.db, user, pk, question_text, choices)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        QuestionService.delete_question(request.db, request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        choice_id = request.data.get("choice_id")
        choice = ChoiceService.vote(request.db, choice_id) 
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
