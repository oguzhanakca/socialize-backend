from django.db import IntegrityError
from rest_framework import serializers
from .models import PostLike, CommentLike


class PostLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
        
    class Meta:
        model = PostLike
        fields = [
            'id', 'owner', 'post', 
            'created_at', 'is_owner',
        ]
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "You've disliked the post."
            })
            
        
        
class CommentLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
        
    class Meta:
        model = CommentLike
        fields = [
            'id', 'owner', 'post', 
            'created_at', 'is_owner',
        ]
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "You've disliked the comment."
            })