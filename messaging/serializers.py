from rest_framework import serializers
from .models import Message, Chat

class MessageSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_image_url = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'owner', 'owner_username', 'owner_image_url', 'content', 'timestamp']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    other_user_username = serializers.SerializerMethodField()
    other_user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'messages', 'other_user_username', 'other_user_profile_image', 'user1', 'user2']

    def get_other_user_username(self, obj):
        request_user = self.context['request'].user
        return obj.user2.username if obj.user1 == request_user else obj.user1.username

    def get_other_user_profile_image(self, obj):
        request_user = self.context['request'].user
        other_user = obj.user2 if obj.user1 == request_user else obj.user1
        return other_user.profile.image.url if hasattr(other_user, 'profile') else None