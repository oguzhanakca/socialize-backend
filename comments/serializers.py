from rest_framework import serializers
from .models import Comment
from likes.models import CommentLike


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = CommentLike.objects.filter(
                owner = user, comment = obj
            ).first()
            return like.id if like else None
        return None
        
    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'post', 'created_at', 'updated_at', 'content',
            'is_owner', 'profile_id', 'profile_image', 'like_id'
        ]
        

class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for detailed view Comment
    """
    post = serializers.ReadOnlyField(source='post.id')
        
