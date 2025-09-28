from rest_framework.decorators import action
from rest_framework.response import Response
from polls.services.stats_service import StatsService
from polls.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework import viewsets

class StatsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def top_question(self, request):
        question = StatsService.get_top_question()
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_choice(self, request):
        choice = StatsService.get_top_choice()
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def question_votes(self, request, pk=None):
        votes = StatsService.get_question_votes(pk)
        return Response({"question_id": pk, "votes": votes})
