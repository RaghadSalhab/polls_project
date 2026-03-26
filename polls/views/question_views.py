from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from polls.services.question_service import QuestionService
from polls.services.choice_service import ChoiceService
from polls.schemas.choice import ChoiceSchema
from rest_framework.permissions import IsAuthenticated

class QuestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        search = request.query_params.get("search")
        questions = QuestionService.list_questions(search)
        return Response(questions)

    def retrieve(self, request, pk=None):
        question = QuestionService.get_question(pk)
        return Response(question)

    def create(self, request):
        user = request.user
        question_text = request.data.get("question_text")
        choices = request.data.get("choices", [])
        question = QuestionService.create_question(user, question_text, choices)
        return Response(question, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        question_text = request.data.get("question_text")
        choices = request.data.get("choices")
        question = QuestionService.update_question(user, pk, question_text, choices)
        return Response(question)

    def destroy(self, request, pk=None):
        QuestionService.delete_question(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        choice_id = request.data.get("choice_id")
        choice = ChoiceService.vote(choice_id)
        return Response(ChoiceSchema().dump(choice))
