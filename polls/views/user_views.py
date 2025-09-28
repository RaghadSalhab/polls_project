from rest_framework import viewsets, status
from rest_framework.response import Response
from polls.services.user_service import UserService
from polls.services.question_service import QuestionService
from polls.serializers import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from polls.serializers import UserQuestionSerializer,QuestionSerializer
# ------------------- Users -------------------
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = UserService.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = UserService.get_user(pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        data = request.data
        try:
            updated_user = UserService.update_user(request.user, pk, **data)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(updated_user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            UserService.delete_user(request.user, pk)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------- Register -------------------
from rest_framework import generics

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        UserService.create_user(username, email, password)

class UserQuestionsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, user_pk=None):
        try:
            questions = QuestionService.list_questions_for_user(user_pk)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        serializer = UserQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        try:
            question = QuestionService.get_question(pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if str(question.created_by.id) != str(user_pk):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)
