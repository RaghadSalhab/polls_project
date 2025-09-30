from rest_framework import viewsets, status
from rest_framework.response import Response
from polls.services.user_service import UserService
from polls.services.question_service import QuestionService
from polls.serializers import UserSerializer, UserRegisterSerializer, UserQuestionSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

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
            return Response({"detail": "Not found"}, status=404)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            updated_user = UserService.update_user(request.user, pk, **request.data)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
        serializer = UserSerializer(updated_user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            UserService.delete_user(request.user, pk)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
        return Response(status=204)


class UserQuestionsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, user_pk=None):
        questions = QuestionService.list_questions_for_user(user_pk)
        serializer = UserQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        question = QuestionService.get_question(pk)
        if str(question.created_by.id) != str(user_pk):
            return Response({"detail": "Not found"}, status=404)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


# ------------------- Register -------------------
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"]
        )
        # توليد التوكن
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
