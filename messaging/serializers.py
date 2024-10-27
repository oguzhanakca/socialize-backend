from rest_framework import serializers
from .models import Message, Chat

class MessageSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_image_url = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'owner', 'owner_username', 'owner_image_url', 'content', 'timestamp']


class ChatSerializer(serializers.ModelSerializer):
    user1_username = serializers.ReadOnlyField(source='user1.username')
    user1_image_url = serializers.ReadOnlyField(source='user1.profile.image.url')
    user2_username = serializers.ReadOnlyField(source='user2.username')
    user2_image_url = serializers.ReadOnlyField(source='user2.profile.image.url')
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user1', 'user2', 'user1_username', 'user1_image_url', 'user2_username', 'user2_image_url', 'messages']