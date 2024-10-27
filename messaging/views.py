from rest_framework import generics, permissions
from socialize_backend.permissions import IsMessageOwnerOrInChat
from django.db.models import Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(user1=user) | Q(user2=user))

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageOwnerOrInChat]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        recipient = serializer.validated_data['owner']
        chat, created = Chat.objects.get_or_create(
            Q(user1=user, user2=recipient) | Q(user1=recipient, user2=user)
        )
        serializer.save(chat=chat)
        
        

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageOwnerOrInChat]

    def get_queryset(self):
        return Message.objects.all()
