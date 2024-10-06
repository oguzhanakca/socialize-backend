from rest_framework import serializers
from .models import Post
import cloudinary.uploader


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(source='image.url', read_only=True)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    
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
        
    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'image_url', 'is_owner', 'profile_id', 'profile_image'
        ]
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        upload_data = cloudinary.uploader.upload(image)
        validated_data['image'] = upload_data['public_id']
        return Post.objects.create(**validated_data)
