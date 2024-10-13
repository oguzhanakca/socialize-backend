from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower
from profiles.models import Profile



class FollowerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_user = serializers.ReadOnlyField(source='followed')
        
    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'followed', 
            'created_at', 'follower_user',
        ]
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "possible duplicate"
            })
