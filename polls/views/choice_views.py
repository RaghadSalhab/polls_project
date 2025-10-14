

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from polls.services.choice_service import ChoiceService
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class ChoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        try:
            choices = ChoiceService.list_choices_for_question(question_pk)
            return Response(choices)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request, question_pk=None):
        try:
            search = request.query_params.get("search")
            if search:
                choices = ChoiceService.search_choices(question_pk, search)
            else:
                choices = ChoiceService.list_choices_for_question(question_pk)
            return Response(choices)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)    

    def create(self, request, question_pk=None):
        choice_text = request.data.get("choice_text")
        try:
            choice = ChoiceService.create_choice(request.user, question_pk, choice_text)
            return Response(choice, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, PermissionDenied) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, question_pk=None):
        choice_text = request.data.get("choice_text")
        try:
            choice = ChoiceService.update_choice(request.user, pk, choice_text)
            return Response(choice)
        except (ObjectDoesNotExist, PermissionDenied) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, question_pk=None):
        try:
            choice = ChoiceService.get_choice(pk)
            return Response(choice)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, question_pk=None):
        try:
            ChoiceService.delete_choice(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (ObjectDoesNotExist, PermissionDenied) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    