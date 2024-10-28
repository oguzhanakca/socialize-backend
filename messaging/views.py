from rest_framework import generics, permissions
from django.db.models import OuterRef, Subquery
from .models import Chat, Message
from django.contrib.auth.models import User
from .serializers import ChatSerializer, MessageSerializer
from socialize_backend.permissions import IsMessageOwnerOrInChat

class ChatListCreateView(generics.ListCreateAPIView):
    """
    List all chats for the current user or create a new chat.
    """
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Subquery to get the timestamp of the last message
        last_message_timestamp = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-timestamp').values('timestamp')[:1]

        # Filter the chats for the current user and order by the last message's timestamp
        return (
            Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)
        ).annotate(
            last_message_time=Subquery(last_message_timestamp)
        ).order_by('-last_message_time')
    
    # def get_queryset(self):
    #     user = self.request.user
    #     return Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)
    
    def perform_create(self, serializer):
        user2_id = self.request.data.get('user2')
        user2 = User.objects.get(id=user2_id)

        serializer.save(user1=self.request.user, user2=user2)

class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a chat.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageListCreateView(generics.ListCreateAPIView):
    """
    List messages for a specific chat or create a new message in a chat.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        print("Creating message for owner:", self.request.user)
        serializer.save(owner=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a message.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsMessageOwnerOrInChat]
