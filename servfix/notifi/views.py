from rest_framework import generics
from .models import Notification,Providerprofile
from .serializer import NotificationSerializer
from notification.models import Post
from rest_framework.views import APIView
from rest_framework.response import Response


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        # Retrieve notifications for the authenticated user
        user = self.request.user
        if hasattr(user,'providerprofile'):
            return Notification.objects.filter(recipient1=user.providerprofile)
        else:
            return Notification.objects.filter(recipient2=user)

    

class NotificationRetrieveView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer






