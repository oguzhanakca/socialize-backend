from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Post
from followers.models import Follower
from likes.models import PostLike
import cloudinary.uploader


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for post model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.CharField(source='image.url', read_only=True)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    postlikes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_private = serializers.ReadOnlyField(source='owner.profile.is_private')
    following_id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size must be lower than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width must be lower than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height must be lower than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = PostLike.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'title', 'content', 'like_id', 'is_private',
            'image', 'image_url', 'is_owner', 'profile_id',
            'profile_image', 'following_id',
            'postlikes_count', 'comments_count'
        ]

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        if image:
            upload_data = cloudinary.uploader.upload(image)
            validated_data['image'] = upload_data['public_id']
        else:
            validated_data['image'] = 'default_post_uu0i5n'

        return Post.objects.create(**validated_data)
