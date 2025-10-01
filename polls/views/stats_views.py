from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.services.stats_service import StatsService
from polls.schemas.question import QuestionSchema
from polls.schemas.choice import ChoiceSchema
from polls.models.database import Session

class StatsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def top_question(self, request):
        result = StatsService.get_top_question()
        if result is None:
            return Response({"detail": "No questions found"}, status=404)
        schema = QuestionSchema()
        data = schema.dump(result)
        return Response(data)

    @action(detail=False, methods=["get"])
    def top_choice(self, request):
        result = StatsService.get_top_choice()
        if result is None:
            return Response({"detail": "No choices found"}, status=404)
        schema = ChoiceSchema()
        data = schema.dump(result)
        return Response(data)

    @action(detail=True, methods=["get"])
    def question_votes(self, request, pk=None):
        votes = StatsService.get_question_votes(pk)
        return Response({"question_id": pk, "votes": votes})

    @action(detail=False, methods=["get"])
    def questions_with_votes(self, request):
        results = StatsService.list_questions_with_votes()
        data = [
            {
                "question": QuestionSchema().dump(q),
                "total_votes": total_votes,
            }
            for q, total_votes in results
        ]
        return Response(data)
