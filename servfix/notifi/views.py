from collections import defaultdict
from rest_framework import generics
from .models import Notification,Providerprofile , ChatNotification
from .serializer import NotificationSerializer , GetChatNotificationSerializer , ChatMessagesSerializer
from notification.models import Post , ChatMessages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q


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
        qs = ChatMessages.objects.filter(recipient=user).order_by('-timestamp')
        for message in qs:
            message.mark_as_seen()
        return qs
    
    




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




class ChatMessagesListView(generics.ListAPIView):
    serializer_class = ChatMessagesSerializer

    def get_queryset(self):
        user = self.request.user
        qs = ChatMessages.objects.filter(Q(recipient=user) | Q(sender=user)).order_by('-timestamp')
        last_messages = defaultdict(lambda:None)
        for message in qs :
            other_users = message.sender if message.sender != user else message.recipient
            if last_messages[other_users] is None or message.timestamp > last_messages[other_users].timestamp:
                last_messages[other_users] = message
        
        queryset = [message for message in last_messages.values() if message]
        return queryset
    

class ChatforspecificpersonListView(generics.ListAPIView):
    serializer_class = ChatMessagesSerializer
    
    def get_queryset(self):
        user1 = self.request.user
        user2 = self.kwargs['user_id']
        queryset = ChatMessages.objects.filter(Q(sender=user1,recipient=user2)| Q(sender=user2,recipient=user1)).order_by('timestamp')
        for message in queryset:
            message.mark_as_seen()
        return queryset 


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request,message_id):
    message = get_object_or_404(ChatMessages,id=message_id)    
    if request.user == message.sender:
        message.delete()
        return Response({'details':'Chat deleted successfully'},status=status.HTTP_200_OK)
    else:
        return Response({'details':'You cannot delete this message'},status=status.HTTP_200_OK)