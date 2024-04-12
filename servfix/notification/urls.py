from . import views
from notification.csrf_view import get_csrf_token_view
from django.urls import path
from .views import *
urlpatterns = [
    path('chat/threads/', ChatThreadListCreateAPIView.as_view(), name='chat-thread-list-create'),
    path('chat/messages/', ChatMessageListCreateAPIView.as_view(), name='chat-message-list-create'),
    path('post_create',views.post_create,name='post_create'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/accept/', PostAcceptAPIView.as_view(), name='post-accept'),
    path('posts/<int:pk>/reject/', PostRejectAPIView.as_view(), name='post-reject'),
    path('chat/end-session/<int:pk>/', EndChatSessionAPIView.as_view(), name='end-chat-session'),
    path('post_accept/<str:post_id>',views.PostAcceptView,name='post_accept'), 
    path('get_accepted_posts',views.get_accepted_posts,name='get_accepted_posts'),
    path('create-post-for-provider/', views.PostForSpecificProviderCreateAPIView, name='post-create'),
    path('posts/<int:post_id>/accept/', views.accept_post, name='accept_post'),
    path('get-csrf-token/', get_csrf_token_view, name='get_csrf_token'),
    path('posts/<int:post_id>/reject/', views.reject_post, name='reject_post'),
    path('<int:notification_id>/delete/', delete_notification, name='delete_notification'),
]
