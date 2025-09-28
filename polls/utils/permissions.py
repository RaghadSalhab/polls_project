# polls_app/utils/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "created_by"):
            return obj.created_by == request.user

        if hasattr(obj, "question"):
            return obj.question.created_by == request.user

        return False
