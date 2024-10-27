from rest_framework import permissions
from followers.models import Follower


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    If profile is private, only profile owner and followers can see posts.
    If not, everyone can read posts and profile owner can CRUD.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return obj.owner == request.user
    
    
