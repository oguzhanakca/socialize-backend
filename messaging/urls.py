from django.urls import path
from .views import ChatListCreateView, MessageListCreateView, MessageDetailView

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]