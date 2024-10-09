from django.db.models import Count
from rest_framework import generics, permissions, filters
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
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        postlikes_count=Count('post_likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    search_fields = [
        'owner__username',
        'title'
    ]
    ordering_filters = [
        'postlikes_count',
        'comments_count',
        'post_likes__created_at'
    ]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve post, edit and delete if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        postlikes_count=Count('post_likes', distinct=True)
    ).order_by('-created_at')
   