from rest_framework import serializers
from .models import Profile
import cloudinary.uploader


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(source='image.url', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'bio', 'image', 'image_url'
        ]
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        # Cloudinary'ye dosyayı yüklüyoruz
        upload_data = cloudinary.uploader.upload(image)
        validated_data['image'] = upload_data['public_id']
        return Profile.objects.create(**validated_data)
