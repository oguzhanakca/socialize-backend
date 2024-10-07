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
        owner = validated_data.get('owner')
        post = validated_data.get('post')
        already_liked = PostLike.objects.filter(owner=owner, post=post).first()
        if already_liked:
            already_liked.delete()
            raise serializers.ValidationError({
                'detail': "You've disliked the post"
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
        owner = validated_data.get('owner')
        comment = validated_data.get('comment')
        already_liked = CommentLike.objects.filter(owner=owner, comment=comment).first()
        if already_liked:
            already_liked.delete()
            raise serializers.ValidationError({
                'detail': "You've disliked the comment"
            })
