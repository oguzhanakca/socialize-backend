from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    If profile is private, only profile owner and followers can see posts.
    If not, everyone can read posts and profile owner can CRUD.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsMessageOwnerOrInChat(permissions.BasePermission):
    """
    Allow access only to the owner of the message or the users in the chat.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (obj.chat.user1 == request.user
                    or obj.chat.user2 == request.user)

        return obj.owner == request.user
