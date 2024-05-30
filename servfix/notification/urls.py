from . import views
from notification.csrf_view import get_csrf_token_view
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
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
    path('get-csrf-token/', get_csrf_token_view, name='get_csrf_token'),
    path('chat/<int:pk>',views.chat,name='chat'),
    path('get_post_by_id/<str:pk>',views.get_post_by_id,name='get_post_by_id'),
    path('post/create/<int:provider_id>/', create_post_and_notification, name='create_post_and_notification'), 
    path('post/accept/<int:post_id>/', accept_post, name='accept_post'), 
    path('post/reject/<int:post_id>/', reject_post, name='reject_post'), 
    path('provider/posts/', get_provider_posts, name='get_provider_posts'), 
    # path('accepted-users-and-providers/', get_accepted_users_and_providers, name='accepted_users_and_providers'), 
    path('immediate-notifications/', get_all_immediate_notifications, name='immediate_notifications'),
    path('delete_chat/<str:chat_id>',views.delete_chat,name='delete_chat'),
    path('get_accepted_users_and_providers',views.accepted_users_and_providers,name='get_accepted_users_and_providers'),
    path('accepted-users-and-providers/', get_accepted_users_and_providers, name='accepted_users_and_providers'),
    path('provider/post/<int:post_id>/', get_post2_by_id, name='get_post_by_id'),
    path('not/post/<str:pk>', get_post_by_id3, name='get_post_by_id'),
    path('terminate_chat/<int:provider_id>/', terminate_chat, name='terminate_chat'),
    path('delete_message/<str:message_id>',views.delete_message,name='delete_message'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
   
    
    
