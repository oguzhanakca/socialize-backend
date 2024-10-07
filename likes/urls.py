from django.urls import path
from likes import views

urlpatterns = [
    path('postlikes/', views.PostLikeList.as_view()),
    path('postlikes/<int:pk>', views.PostLikeDetail.as_view()),
    path('commentlikes/', views.CommentLikeList.as_view()),
    path('commentlikes/<int:pk>', views.CommentLikeDetail.as_view()),
    
]
