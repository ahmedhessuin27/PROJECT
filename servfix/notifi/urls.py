from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('allnotification/',views.NotificationListView.as_view(),name='AllNotifications'),
    path('notification/<str:pk>',views.NotificationRetrieveView.as_view(),name='Notification_lists'),
    path('Chatmessages',views.ChatMessagesListView.as_view(),name='Chatmessages'),
    path('chatnotification',views.ChatNotificationsListView.as_view(),name='chatnotification'),
    path('delete_notification/<str:notifi_id>',views.delete_notification,name='delete_notification'),
    path('Chatmessages',views.ChatMessagesListView.as_view(),name='Chatmessages'),
    path('chatforspecificperson/<str:user_id>',views.ChatforspecificpersonListView.as_view(),name='chatforspecificperson'),
    path('delete_message/<str:message_id>',views.delete_message,name='delete_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)