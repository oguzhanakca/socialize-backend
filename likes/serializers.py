from django.db import IntegrityError
from rest_framework import serializers
from .models import PostLike, CommentLike


class PostLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
        
    class Meta:
        model = PostLike
        fields = [
            'id', 'owner', 'post', 
            'created_at',
        ]
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "possible duplicate"
            })
            
        
        
class CommentLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
        
    class Meta:
        model = CommentLike
        fields = [
            'id', 'owner', 'comment', 
            'created_at'
        ]
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "possible duplicate"
            })