from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import ChatThreadSerializer, ChatMessageSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

class ChatThreadListCreateAPIView(generics.ListCreateAPIView):
    queryset = ChatThread.objects.all()
    serializer_class = ChatThreadSerializer
    #permission_classes = [IsAuthenticated]




class ChatMessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Extract user ID from the request data
        user_id = self.request.data.get('sender')
        
        # Retrieve the user object based on the user ID
        try:
            sender_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Handle the case where the user does not exist
            raise ValueError('User with ID {} does not exist'.format(user_id))
        
        # Set the sender field with the retrieved user object
        serializer.save(sender=sender_user)

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
   


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostAcceptAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
   

class PostRejectAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    
class EndChatSessionAPIView(generics.UpdateAPIView):
    queryset = ChatThread.objects.all()
    serializer_class = ChatThreadSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_ended = True  # Assuming you have a field 'is_ended' in your ChatThread model
        instance.save()
        return Response({'detail': 'Chat session ended successfully'}, status=status.HTTP_200_OK)