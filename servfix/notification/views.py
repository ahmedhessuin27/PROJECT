from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.views.decorators.csrf import csrf_protect

from notifi.models import Notification
from notifi.serializer import NotificationSerializer
from .models import *
from .serializers import ChatThreadSerializer, ChatMessageSerializer, PostForSpecificProviderSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostForSpecificProviderSerializer,PostNewsSerializer,AcceptedPostsSerializer,PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post,PostNews,PostForSpecificProvider
from django.shortcuts import get_object_or_404



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

class PostCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    


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
    
    
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PostAcceptView(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    provider = Providerprofile.objects.get(user=request.user)
    if PostNews.objects.filter(post=post,provider=provider,status='accepted').exists():
        return Response({'details':'This post has already been accepted'},status=status.HTTP_400_BAD_REQUEST)
    else:
        post_status = PostNews.objects.create(user=post.user,provider=provider,post=post,status='accepted')
        serializer = PostNewsSerializer(post_status)
        return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accepted_posts(request):
    provider = Providerprofile.objects.get(user=request.user)
    accepted_posts = PostNews.objects.all().filter(provider=provider)
    serializer = AcceptedPostsSerializer(accepted_posts,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def PostForSpecificProviderCreateAPIView(request):
    serializer = PostForSpecificProviderSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()

        sender = post.user
        recipient = post.provider.user if post.provider.user else post.user  # Use provider's user if available, else use post's user
        is_from_provider = False
        
        if post.accepted:
            message = f"{post.provider.username} accepted your post."
        elif post.rejected:
            message = f"{post.provider.username} rejected your post."
        else:
            message = post.message
        
        ImmediateNotification.objects.create(
            sender=sender,
            recipient=recipient,
            message=message,
            image=post.image,  
            is_from_provider=post.accepted or post.rejected,
            related_post=post
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reject_post(request, post_id):
    post = get_object_or_404(PostForSpecificProvider, pk=post_id)
    post.rejected = True
    post.save()
    
    sender = post.provider.user if post.provider.user else post.user
    
    ImmediateNotification.objects.create(
        sender=sender,
        recipient=post.user,
        message=f"{sender.username} rejected your post.",
        image=post.image,  
        is_from_provider=True,
        related_post=post
    )
    
    return Response({"message": "Post rejected successfully."}, status=status.HTTP_200_OK)

# accept post
@api_view(['POST'])
def accept_post(request, post_id):
    post = get_object_or_404(PostForSpecificProvider, pk=post_id)
    post.accepted = True
    
    with transaction.atomic():
        post.save()
        
        sender = post.provider.user  
        
        ImmediateNotification.objects.create(
            sender=sender,
            recipient=post.user,
            message=f"{sender.username} accepted your post.",
            image=post.image,  
            is_from_provider=True,
            related_post=post
        )
    
   
    return Response({"message": "Post accepted successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    notification = get_object_or_404(ImmediateNotification, pk=notification_id)
    
    if request.user != notification.sender:
        return Response({"message": "You are not authorized to delete this notification."}, status=403)
    
    notification.delete()
    
    return Response({"message": "Notification deleted successfully."}, status=200)