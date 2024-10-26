from rest_framework import serializers
from .models import Profile
from followers.models import Follower
import cloudinary.uploader


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(source='image.url', read_only=True)
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    followed_by_current_user = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner = user, followed = obj.owner
            ).first()
            return following.id if following else None
        return None
    
    def get_followed_by_current_user(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follower.objects.filter(owner=user, followed=obj.owner).exists()
        return False
        
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'bio', 'is_private',
            'image', 'image_url', 'is_owner', 'following_id', 'posts_count', 'followed_by_current_user',
            'followers_count', 'following_count'
        ]
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        upload_data = cloudinary.uploader.upload(image)
        validated_data['image'] = upload_data['public_id']
        return Profile.objects.create(**validated_data)
