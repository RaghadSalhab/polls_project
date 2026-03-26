from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.services.stats_service import StatsService

class StatsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def top_question(self, request):
        result = StatsService.get_top_question()
        if not result:
            return Response({"detail": "No questions found"}, status=404)
        return Response(result)

    @action(detail=False, methods=["get"])
    def top_choice(self, request):
        result = StatsService.get_top_choice()
        if not result:
            return Response({"detail": "No choices found"}, status=404)
        return Response(result)

    @action(detail=True, methods=["get"])
    def question_votes(self, request, pk=None):
        votes = StatsService.get_question_votes(pk)
        return Response({"question_id": pk, "votes": votes})

    @action(detail=False, methods=["get"])
    def questions_with_votes(self, request):
        results = StatsService.list_questions_with_votes()
        return Response(results)
