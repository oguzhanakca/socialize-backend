from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message

@receiver(post_save, sender=Message)
def update_chat_last_message_time(sender, instance, **kwargs):
    chat = instance.chat
    chat.last_message_time = instance.timestamp
    chat.save()