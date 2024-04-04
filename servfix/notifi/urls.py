from django.urls import path
from . import views

urlpatterns = [
    path('allnotification/',views.NotificationListView.as_view(),name='AllNotifications'),
    path('notification/<str:pk>',views.NotificationRetrieveView.as_view(),name='Notification_lists'),
]