from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.views.decorators.csrf import csrf_protect

from notifi.models import Notification
from notifi.serializer import NotificationSerializer
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def post_create(request): 
    data = request.data 
 
    required_fields = ['service_name', 'problem_description', 'city'] 
    missing_fields = [field for field in required_fields if field not in data or not data[field]] 
 
    if missing_fields: 
        return Response({'error': f"The following fields are required: {', '.join(missing_fields)}"},  
                        status=status.HTTP_400_BAD_REQUEST) 
 
    try: 
        service = Service.objects.get(name=data['service_name']) 
    except Service.DoesNotExist: 
        return Response({'error': 'Service does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    user = Userprofile.objects.get(user=request.user) 
    Post.objects.create( 
        user=user, 
        service=service, 
        image=data['image'], 
        service_name=data['service_name'], 
        problem_description=data['problem_description'], 
        city=data['city'] 
    ) 
 
    return Response({'success': 'Post created successfully'}, status=status.HTTP_201_CREATED)
    


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


api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
# @csrf_exempt 
def create_post_and_notification(request, provider_id): 
    try: 
        user_profile = request.user.userprofile 
         
        provider_profile = Providerprofile.objects.get(pk=provider_id) 
    except Providerprofile.DoesNotExist: 
        return Response({'error': 'Provider profile does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    post_data = { 
        'user': user_profile.id, 
        'provider': provider_profile.id, 
        'message': request.data.get('message', ''), 
        'image': request.data.get('image', None) 
    } 
    post_serializer = PostForSpecificProviderSerializer(data=post_data) 
    if post_serializer.is_valid(): 
        post = post_serializer.save() 
 
        notification_data = { 
            'sender': user_profile.id, 
            'recipient': provider_profile.id, 
            'message': f"{user_profile.username} posted for you specially: {request.data.get('message', '')}", 
            'image': post.image, 
            'related_post': post.id, 
            'is_from_provider': False   
        } 
        notification_serializer = ImmediateNotificationSerializer(data=notification_data) 
        if notification_serializer.is_valid(): 
            notification_serializer.save() 
            return Response(post_serializer.data, status=status.HTTP_201_CREATED) 
        else: 
            post.delete()   
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    else: 
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def reject_post(request, post_id): 
    try: 
        post = PostForSpecificProvider.objects.get(pk=post_id) 
         
        if request.user != post.provider.user: 
            return Response({'error': 'You are not authorized to reject this post'}, status=status.HTTP_403_FORBIDDEN) 
         
        # reason = request.data.get('reason', '') 
         
        post.rejected = True   
        post.save() 
         
        notification_data = { 
            'sender': post.provider.id,   
            'recipient': post.user.id, 
            'message': "Your post has been rejected", 
            'related_post': post.id, 
            'is_from_provider': True,   
            'rejected': True,   
            'image': post.image   
        } 
        notification_serializer = ImmediateNotificationSerializer(data=notification_data) 
        if notification_serializer.is_valid(): 
            notification_serializer.save() 
            return Response({'message': 'Post rejected successfully'}, status=status.HTTP_200_OK)
        else: 
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except PostForSpecificProvider.DoesNotExist: 
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 


# accept post
@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
# @csrf_exempt 
def accept_post(request, post_id): 
    try: 
        post = PostForSpecificProvider.objects.get(pk=post_id) 
         
        if post.provider.user != request.user: 
            return Response({'error': 'You are not authorized to accept this post'}, status=status.HTTP_403_FORBIDDEN) 
         
        post.accepted = True 
        post.save() 
         
        notification_data = { 
            'sender': post.provider.id,   
            'recipient': post.user.id, 
            'message': f"Your post has been accepted by {post.provider.username}", 
            'related_post': post.id, 
            'is_from_provider': True   
        } 
         
        if post.image: 
            notification_data['image'] = post.image 
         
        notification_serializer = ImmediateNotificationSerializer(data=notification_data) 
        if notification_serializer.is_valid(): 
            notification_serializer.save() 
            return Response({'message': 'Post accepted successfully'}, status=status.HTTP_200_OK) 
        else: 
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except PostForSpecificProvider.DoesNotExist: 
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND) 


class NotificationDeleteAPIView(generics.DestroyAPIView): 
    queryset = ImmediateNotification.objects.all() 
    serializer_class = NotificationDeleteSerializer 
 
    def delete(self, request, *args, **kwargs): 
        notification = self.get_object() 
        notification.delete() 
        return Response({'message': 'Notification deleted successfully'}, status=status.HTTP_204_NO_CONTENT)