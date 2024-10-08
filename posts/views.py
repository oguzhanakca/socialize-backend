from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from socialize_backend.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    List posts and create posts if you're logged in
    """
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve post, edit and delete if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
   