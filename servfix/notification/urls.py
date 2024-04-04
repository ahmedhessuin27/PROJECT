from . import views

from django.urls import path
from .views import *
urlpatterns = [
    path('chat/threads/', ChatThreadListCreateAPIView.as_view(), name='chat-thread-list-create'),
    path('chat/messages/', ChatMessageListCreateAPIView.as_view(), name='chat-message-list-create'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/accept/', PostAcceptAPIView.as_view(), name='post-accept'),
    path('posts/<int:pk>/reject/', PostRejectAPIView.as_view(), name='post-reject'),
    path('chat/end-session/<int:pk>/', EndChatSessionAPIView.as_view(), name='end-chat-session'),
    path('post_accept/<str:post_id>',views.PostAcceptView,name='post_accept'), 
    path('get_accepted_posts',views.get_accepted_posts,name='get_accepted_posts'),
]
