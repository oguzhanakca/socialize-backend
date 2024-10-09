from django.db.models import Count
from rest_framework import generics, permissions, filters
from socialize_backend.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentDetailSerializer, CommentSerializer


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.annotate(
        commentlikes_count=Count('comment_likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_filters = [
        'commentlikes_count',
        'comment_likes__created_at'
    ]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.annotate(
        commentlikes_count=Count('comment_likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_filters = [
        'commentlikes_count',
        'comment_likes__created_at'
    ]
