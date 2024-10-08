from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from socialize_backend.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrive or update a profile you own.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()