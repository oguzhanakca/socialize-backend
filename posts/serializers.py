from rest_framework import serializers
from .models import Post
from likes.models import PostLike
import cloudinary.uploader


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.CharField(source='image.url', read_only=True)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    postlikes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    
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
                owner = user, post = obj
            ).first()
            return like.id if like else None
        return None
        
    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content', 'like_id',
            'image', 'image_url', 'image_filter', 'is_owner', 'profile_id', 'profile_image',
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
