from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from polls.services.user_service import UserService
from polls.services.question_service import QuestionService
from polls.schemas.user import UserSchema
from polls.schemas.question import QuestionSchema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from polls.models.database import Session

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = UserService.list_users()
        schema = UserSchema(many=True)
        data = schema.dump(users)
        return Response(data)

    def retrieve(self, request, pk=None):
        try:
            user = UserService.get_user(pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        schema = UserSchema()
        data = schema.dump(user)
        return Response(data)

    def update(self, request, pk=None):
        try:
            updated_user = UserService.update_user(request.user, pk, **request.data)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
        schema = UserSchema()
        data = schema.dump(updated_user)
        return Response(data)

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
        schema = QuestionSchema(many=True)
        data = schema.dump(questions)
        return Response(data)

    def retrieve(self, request, pk=None, user_pk=None):
        question = QuestionService.get_question(pk)
        if str(question.created_by.id) != str(user_pk):
            return Response({"detail": "Not found"}, status=404)
        schema = QuestionSchema()
        data = schema.dump(question)
        return Response(data)
    
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        from marshmallow import ValidationError
        from polls.schemas.user import UserSchema

        schema = UserSchema()
        try:
            user_data = schema.load(request.data)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=400)

        user = UserService.create_user(
            user_data["username"],
            user_data["email"],
            user_data["password"]
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": schema.dump(user),
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)