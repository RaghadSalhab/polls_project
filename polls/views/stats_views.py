from rest_framework.decorators import action
from rest_framework.response import Response
from polls.services.stats_service import StatsService
from polls.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework import viewsets

class StatsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def top_question(self, request):
        result = StatsService.get_top_question(request.db)
        if result is None:
            return Response({"detail": "No questions found"}, status=404)
        serializer = QuestionSerializer(result)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_choice(self, request):
        result = StatsService.get_top_choice(request.db)
        if result is None:
            return Response({"detail": "No choices found"}, status=404)
        serializer = ChoiceSerializer(result)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def question_votes(self, request, pk=None):
        votes = StatsService.get_question_votes(request.db, pk)
        return Response({"question_id": pk, "votes": votes})

    @action(detail=False, methods=["get"])
    def questions_with_votes(self, request):
        results = StatsService.list_questions_with_votes(request.db)
        data = [
            {
                "question": QuestionSerializer(q).data,
                "total_votes": total_votes,
            }
            for q, total_votes in results
        ]
        return Response(data)
