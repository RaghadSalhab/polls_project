# polls/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from polls.views.question_views import QuestionViewSet, ChoiceViewSet
from polls.views.user_views import UserViewSet, UserQuestionsViewSet

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'users', UserViewSet, basename='users')

# nested: /questions/{question_id}/choices/
choices_router = routers.NestedDefaultRouter(router, r'questions', lookup='question')
choices_router.register(r'choices', ChoiceViewSet, basename='question-choices')

# nested: /users/{user_id}/questions/
user_questions_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
user_questions_router.register(r'questions', UserQuestionsViewSet, basename='user-questions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(choices_router.urls)),
    path('', include(user_questions_router.urls)),
]
