from rest_framework import permissions
from django.contrib.auth.models import User

class IsUpdateHighScore(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs["pk"])
        if request.user == user:
            return True
        return False