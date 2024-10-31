from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    """
    Chat model
    """
    user1 = models.ForeignKey(
        User, related_name='chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='chat_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Chat between {self.user1.username} and {self.user2.username}'


class Message(models.Model):
    """
    Message model
    """
    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.owner.username}'
