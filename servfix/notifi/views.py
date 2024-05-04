from rest_framework import generics
from .models import Notification,Providerprofile , ChatNotification
from .serializer import NotificationSerializer , GetChatNotificationSerializer , ChatMessagesSerializer
from notification.models import Post 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        # Retrieve notifications for the authenticated user
        user = self.request.user
        if hasattr(user,'providerprofile'):
            return  Notification.objects.filter(recipient1=user.providerprofile).order_by('-created_at')
        else:
            return Notification.objects.filter(recipient2=user.userprofile).order_by('-created_at')

    

class NotificationRetrieveView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer





class ChatMessagesListView(generics.ListAPIView):
    serializer_class = ChatMessagesSerializer
    
    def get_queryset(self):
        user = self.request.user
        return ChatNotification.objects.filter(recipient=user).order_by('-created_at')
    
    




class ChatNotificationsListView(generics.ListAPIView):
    serializer_class = GetChatNotificationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return ChatNotification.objects.filter(recipient=user).order_by('-created_at')
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request,notifi_id):
    notification = get_object_or_404(Notification,id=notifi_id)
    notification.delete()
    return Response({'details':'the notification deleted successfully'},status=status.HTTP_200_OK)    
