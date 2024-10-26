from django.db import models
from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from socialize_backend.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles
    """
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend   
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]
    ordering_fields = [
        'posts_count', 'followers_count', 'following_count',
        'owner__following__created_at', 'owner__followed__created_at'
    ]
    def get_queryset(self):
        user = self.request.user
        
        return Profile.objects.annotate(
            posts_count=Count('owner__post', distinct=True),followers_count=Count('owner__followed', distinct=True),following_count=Count('owner__following', distinct=True)
            ).filter(models.Q(is_private=False) | models.Q(owner__following__followed=user)).order_by('-created_at')
    
    

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrive or update a profile you own.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        user = self.request.user
        return Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).filter(models.Q(is_private=False) | models.Q(owner__following__followed=user)).order_by('-created_at')
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)  
        self.perform_update(serializer)

        return Response(serializer.data)