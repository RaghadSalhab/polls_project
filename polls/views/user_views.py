from marshmallow import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from polls.schemas.user import UserSchema
from polls.services.user_service import UserService
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from polls.services.user_service import UserService
from polls.services.question_service import QuestionService

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = UserService.list_users()
        return Response(users)

    def retrieve(self, request, pk=None):
        try:
            user = UserService.get_user(pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        return Response(user)

    def update(self, request, pk=None):
        try:
            updated_user = UserService.update_user(request.user, pk, **request.data)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
        return Response(updated_user)

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
        return Response(questions)

    def retrieve(self, request, pk=None, user_pk=None):
        question = QuestionService.get_question(pk)
        if not question or str(question["created_by"]["id"]) != str(user_pk):
            return Response({"detail": "Not found"}, status=404)
        return Response(question)



    
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        schema = UserSchema()
        try:
            user = schema.load(request.data) 
        except ValidationError as e:
            return Response({"errors": e.messages}, status=400)

        user = UserService.create_user(
            user.username,
            user.email,
            user.password
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": schema.dump(user),
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
