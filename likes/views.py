from rest_framework import generics, permissions
from socialize_backend.permissions import IsOwnerOrReadOnly
from likes.models import PostLike, CommentLike
from likes.serializers import PostLikeSerializer, CommentLikeSerializer


class PostLikeList(generics.ListCreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PostLike.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class PostLikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or Delete your own likes from Post.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()
    
    
class CommentLikeList(generics.ListCreateAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CommentLike.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class CommentLikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or Delete your own likes from Comment.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()