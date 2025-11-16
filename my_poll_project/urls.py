from django.contrib import admin
from django.urls import path, include
from polls.views.user_views import UserRegisterView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

urlpatterns = [
    # path('ai-proxy/', include('ai_proxy.urls')),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
    
]
