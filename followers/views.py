from rest_framework import generics, permissions
from socialize_backend.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    """
    List all followers
    """
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Follower.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    Unfollow if you follow someone
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    
class FollowingList(generics.ListAPIView):
    """
    List users who are following the current logged-in user
    """
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(followed=self.request.user)
