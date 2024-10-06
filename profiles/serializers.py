from rest_framework import serializers
from .models import Profile
import cloudinary.uploader


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(source='image.url', read_only=True)
    is_owner = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
        
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'bio',
            'image', 'image_url', 'is_owner'
        ]
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        upload_data = cloudinary.uploader.upload(image)
        validated_data['image'] = upload_data['public_id']
        return Profile.objects.create(**validated_data)
