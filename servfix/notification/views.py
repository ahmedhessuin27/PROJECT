from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from .filtters import ChatFilter
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
from django.db.models import Q



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
        PostNews.objects.create(user=post.user,provider=provider,post=post,status='accepted')
        return Response({'details':'The post accepted successfully'},status=status.HTTP_200_OK)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accepted_posts(request):
    provider = Providerprofile.objects.get(user=request.user)
    accepted_posts = PostNews.objects.all().filter(provider=provider)
    serializer = AcceptedPostsSerializer(accepted_posts,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
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
            'user_recipient': None, 
            'provider_recipient': provider_profile.id, 
            # 'provider_recipient': None, 
            'message': f"  New post sent for you by {user_profile.user.username}", 
            'image': post.image, 
            'post': post.id 
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
        with transaction.atomic(): 
            post = PostForSpecificProvider.objects.select_for_update().get(pk=post_id) 
 
            if request.user != post.provider.user: 
                return Response({'error': 'You are not authorized to reject this post'}, status=status.HTTP_403_FORBIDDEN) 
 
            if PostForSpecificProviderNews.objects.filter(post_id=post_id, provider_id=request.user.providerprofile.id, status='accepted').exists(): 
                return Response({'error': 'You have accepted this post before'}, status=status.HTTP_400_BAD_REQUEST) 
 
            if PostForSpecificProviderNews.objects.filter(post_id=post_id, provider_id=request.user.providerprofile.id, status='rejected').exists(): 
                return Response({'error': 'This post has already been rejected'}, status=status.HTTP_400_BAD_REQUEST) 
 
            post.rejected = True 
            post.save() 
 
            PostForSpecificProviderNews.objects.create( 
                status='rejected', 
                user_id=post.user.id, 
                provider_id=request.user.providerprofile.id, 
                post_id=post.id 
            ) 
 
            notification_data = { 
                'user_recipient': post.user.id, 
                'message': "Your post has been rejected", 
                'post': post.id, 
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
    except AttributeError as e: 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
 
 
 
 
 
 
 
@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def accept_post(request, post_id): 
    try: 
        with transaction.atomic(): 
            post = PostForSpecificProvider.objects.select_for_update().get(pk=post_id) 
 
            if request.user != post.provider.user: 
                return Response({'error': 'You are not authorized to accept this post'}, status=status.HTTP_403_FORBIDDEN) 
 
            # Check if the post has been rejected before 
            if PostForSpecificProviderNews.objects.filter(post_id=post_id, provider_id=request.user.providerprofile.id, status='rejected').exists(): 
                return Response({'error': 'You have rejected this post before'}, status=status.HTTP_400_BAD_REQUEST) 
 
            if PostForSpecificProviderNews.objects.filter(post_id=post_id, status='accepted').exists(): 
                return Response({'details': 'This post has already been accepted'}, status=status.HTTP_400_BAD_REQUEST) 
 
            # Allow the provider to accept the post 
            PostForSpecificProviderNews.objects.create( 
                status='accepted', 
                user_id=post.user.id, 
                provider_id=request.user.providerprofile.id, 
                post_id=post.id 
            ) 
 
            notification_data = { 
                'user_recipient': post.user.id, 
                'message': "Your post has been accepted", 
                'post': post.id, 
                'image': post.image 
            } 
            notification_serializer = ImmediateNotificationSerializer(data=notification_data) 
            if notification_serializer.is_valid(): 
                notification_serializer.save() 
 
                if hasattr(post.user, 'userprofile'): 
                    token = post.user.userprofile.fcm_token 
                    title = "Post Accepted" 
                    body = "Your post has been accepted" 
                    subtitle = None 
                    if token: 
                        send_fcm_notification(token, title, body, subtitle) 
 
                return Response({'message': 'Post accepted successfully'}, status=status.HTTP_200_OK) 
            else: 
                return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    except PostForSpecificProvider.DoesNotExist: 
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    except AttributeError as e: 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def get_provider_posts(request): 
    try: 
        user = request.user 
        if hasattr(user, 'providerprofile'): 
            provider_id = user.providerprofile.id 
            provider_posts = PostForSpecificProvider.objects.filter(provider_id=provider_id).order_by('-created_at') 
 
            serializer = PostForSpecificProviderSerializer(provider_posts, many=True) 
 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else: 
            return Response({'error': 'User is not a provider'}, status=status.HTTP_400_BAD_REQUEST) 
    except PostForSpecificProvider.DoesNotExist: 
        return Response({'error': 'No posts found for this provider'}, status=status.HTTP_404_NOT_FOUND)
     
 
     
     



@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def chat(request,pk):
    data = request.data
    user = request.user
    recipient = get_object_or_404(User,pk=pk)
    ChatMessages.objects.create(
        sender = user,
        recipient = recipient,
        content = data['content']   
    )
    return Response({'details':'chat done successfully'},status=status.HTTP_200_OK)

        



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_post_by_id(request,pk):
    post = Post.objects.filter(id=pk)
    serializer = RelatedAcceptedPostsSerializer(post, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_post_by_id3(request,pk):
    post = PostForSpecificProvider.objects.filter(id=pk)
    serializer = RelatedPostsSerializer(post, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request,chat_id):
    chat = get_object_or_404(ChatMessages,id=chat_id)    
    chat.delete()
    return Response({'details':'chat deleted successfully'},status=status.HTTP_200_OK)


        

# @api_view(['GET']) 
# @permission_classes([IsAuthenticated]) 
# def get_accepted_users_and_providers(request): 
#     user = request.user 
#     if hasattr(user, 'providerprofile'): 
#         provider_id = user.providerprofile.id 
#         accepted_users = PostForSpecificProviderNews.objects.filter(status='accepted', provider_id=provider_id).values_list('user_id', flat=True) 
#         users_data = [] 
#         for user_id in accepted_users: 
#             user_profile = Userprofile.objects.get(id=user_id)
#             users_data.append({ 
#                 'user_id': user_profile.id, 
#                 'username': user_profile.username, 
#                 'image': user_profile.image.url if user_profile.image else None,
#                 'id': user_profile.user_id

#             }) 
#         data = {'accepted_users': users_data} 
#         if request.GET:
#             filtered_data = ChatFilter(request.GET, queryset=Userprofile.objects.filter(id__in=accepted_users)).qs    
#             serialized_data = []
#             for item in filtered_data:
#                 serialized_data.append({
#                     'user_id': item.id,
#                     'username': item.username,
#                     'image': item.image.url if item.image else None,
#                     'id': item.user_id

#                 })
#             data= {'accepted_users': serialized_data}    
#             return Response(data)
#         else:
#             return Response(data)
#     else: 
#         user_id = user.userprofile.id 
#         accepted_providers = PostForSpecificProviderNews.objects.filter(status='accepted', user_id=user_id).values_list('provider_id', flat=True) 
#         providers_data = [] 
#         for provider_id in accepted_providers: 
#             provider_profile = Providerprofile.objects.get(id=provider_id) 
#             providers_data.append({ 
#                  'provider_id': provider_profile.id, 
#                 'name': provider_profile.username, 
#                 'image': provider_profile.image.url if provider_profile.image else None,
#                 'id': provider_profile.user_id

#             }) 
#         data = {'accepted_providers': providers_data} 
#         if request.GET:
#             filtered_data = ChatFilter(request.GET, queryset=Providerprofile.objects.filter(id__in=accepted_providers)).qs    
#             serialized_data = []
#             for item in filtered_data:
#                 serialized_data.append({
#                     'user_id': item.id,
#                     'username': item.username,
#                     'image': item.image.url if item.image else None,
#                     'id': item.user_id

#                 })
#             data = {'accepted_providers': serialized_data}
#             return Response(data)
#         else:
#             return Response(data)
 
 
@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def get_all_immediate_notifications(request): 
    user = request.user 
    if hasattr(user, 'providerprofile'): 
        notifications = ImmediateNotification.objects.filter(provider_recipient=user.providerprofile) 
    else: 
        notifications = ImmediateNotification.objects.filter(user_recipient=user.userprofile) 
     
    notifications = notifications.order_by('-created_at') 
     
    serializer = ImmediateNotificationSerializer(notifications, many=True) 
    return Response(serializer.data)

# @api_view(['GET']) 
# @permission_classes([IsAuthenticated]) 
# def get_all_immediate_notifications(request): 
#     user = request.user 
#     if hasattr(user, 'providerprofile'): 
#         notifications = ImmediateNotification.objects.filter(provider_recipient=user.providerprofile) 
#     else: 
#         notifications = ImmediateNotification.objects.filter(user_recipient=user.userprofile) 
     
#     notifications = notifications.order_by('-created_at') 

#     serialized_data = []
    
#     for notification in notifications:
#         data = {
#             'message': notification.message,
#             'post_id': notification.post_id,  
#         }
#         serialized_data.append(data)
    
#     return Response(serialized_data)




@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def get_post2_by_id(request, post_id): 
    try: 
        user = request.user 
        if hasattr(user, 'providerprofile'): 
            provider_id = user.providerprofile.id 
            post = PostForSpecificProvider.objects.get(id=post_id, provider_id=provider_id) 
            serializer = PostForSpecificProviderSerializer(post) 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else: 
            return Response({'error': 'User is not a provider'}, status=status.HTTP_400_BAD_REQUEST) 
    except PostForSpecificProvider.DoesNotExist: 
        return Response({'error': 'No post found with this ID for the authenticated provider'}, status=status.HTTP_404_NOT_FOUND)
    


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def terminate_chat(request, provider_id):
#     if not hasattr(request.user, 'userprofile'):
#         return Response({'error': 'User does not have a valid profile.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user_id = request.user.userprofile.id
    
    
#     posts_specific_provider = PostForSpecificProviderNews.objects.filter(user_id=user_id, provider_id=provider_id, status='accepted')
#     posts_general = PostNews.objects.filter(user_id=user_id, provider_id=provider_id, status='accepted')
#     # delete_chat = ChatMessages.objects.filter(Q(sender=request.user.userprofile.user_id,recipient=request.user.providerprofile.user_id)| Q(sender=request.user.providerprofile.user_id,recipient=request.user.userprofile.user_id))
    
#     if posts_specific_provider.exists() or posts_general.exists():
#         if posts_specific_provider.exists():
#             posts_specific_provider.delete()
#             # delete_chat.delete()
#         if posts_general.exists():
#             posts_general.delete()
#             # delete_chat.delete()
#         return Response({'message': 'Chat terminated successfully.'})
#     else:
#         return Response({'message': 'No accepted chats found for termination.'})  



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def terminate_chat(request, provider_id):
    if not hasattr(request.user, 'userprofile'):
        return Response({'error': 'User does not have a valid profile.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.user.userprofile.id
    user_auth_user = request.user.userprofile.user_id
    provider = Providerprofile.objects.get(id=provider_id)
    provider_auth_user = provider.user_id
    
    posts_specific_provider = PostForSpecificProviderNews.objects.filter(user_id=user_id, provider_id=provider_id, status='accepted')
    posts_general = PostNews.objects.filter(user_id=user_id, provider_id=provider_id, status='accepted')
    delete_chat = ChatMessages.objects.filter(Q(sender=user_auth_user,recipient=provider_auth_user)| Q(sender=provider_auth_user,recipient=user_auth_user))
    
    if posts_specific_provider.exists() or posts_general.exists():
        if posts_specific_provider.exists():
            posts_specific_provider.delete()
            delete_chat.delete()
        if posts_general.exists():
            posts_general.delete()
            delete_chat.delete()
        return Response({'message': 'Chat terminated successfully.'})
    else:
        return Response({'message': 'No accepted chats found for termination.'})
    



# @api_view(['GET']) 
# @permission_classes([IsAuthenticated]) 
# def accepted_users_and_providers(request): 
#     user = request.user 
#     if hasattr(user, 'providerprofile'): 
#         provider_id = user.providerprofile.id 
#         accepted_users = PostNews.objects.filter(status='accepted', provider_id=provider_id).values_list('user_id', flat=True) 
#         users_data = [] 
#         seen_users_ids = set()
#         for user_id in accepted_users:
#             if user_id not in seen_users_ids:
#                 seen_users_ids.add(user_id) 
#                 user_profile = Userprofile.objects.get(id=user_id) 
#                 users_data.append({ 
#                     'user_id': user_profile.id, 
#                     'username': user_profile.username, 
#                     'image': user_profile.image.url if user_profile.image else None,
#                     'id' : user_profile.user_id
#                 }) 
#         data = {'accepted_users': users_data}  
        
#         if request.GET:
#             filtered_data = ChatFilter(request.GET, queryset=Userprofile.objects.filter(id__in=accepted_users)).qs    
#             serialized_data = []
#             for item in filtered_data:
#                 serialized_data.append({
#                     'user_id': item.id,
#                     'username': item.username,
#                     'image': item.image.url if item.image else None,
#                     'id' : item.user_id
#                 })
#             return Response(serialized_data)
#         else:
#             return Response(data)
        
#     else: 
#         user_id = user.userprofile.id 
#         accepted_providers = PostNews.objects.filter(status='accepted', user_id=user_id).values_list('provider_id', flat=True) 
#         providers_data = [] 
#         seen_providers_ids = set()
#         for provider_id in accepted_providers: 
#             if provider_id not in seen_providers_ids:
#                 seen_providers_ids.add(provider_id)
#                 provider_profile = Providerprofile.objects.get(id=provider_id) 
#                 providers_data.append({ 
#                     'provider_id': provider_profile.id, 
#                     'name': provider_profile.username, 
#                     'image': provider_profile.image.url if provider_profile.image else None,
#                     'id' : provider_profile.user_id
#                 }) 
#         data = {'accepted_providers': providers_data} 
        
#         if request.GET:
#             filtered_data = ChatFilter(request.GET, queryset=Providerprofile.objects.filter(id__in=accepted_providers)).qs    
#             serialized_data = []
#             for item in filtered_data:
#                 serialized_data.append({
#                     'user_id': item.id,
#                     'username': item.username,
#                     'image': item.image.url if item.image else None,
#                     'id' : item.user_id
#                 })
#             return Response(serialized_data)
#         else:
#             return Response(data)  



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request,message_id):
    message = get_object_or_404(ChatMessages,id=message_id)    
    if request.user == message.sender:
        message.delete()
        return Response({'details':'Chat deleted successfully'},status=status.HTTP_200_OK)
    else:
        return Response({'details':'You cannot delete this message'},status=status.HTTP_200_OK)  





@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def accepted_users_and_providers(request): 
    user = request.user 
    if hasattr(user, 'providerprofile'): 
        provider_id = user.providerprofile.id 
        accepted_users_all = PostNews.objects.filter(status='accepted', provider_id=provider_id).values_list('user_id', flat=True) 
        accepted_users_specific = PostForSpecificProviderNews.objects.filter(status='accepted',provider_id=provider_id).values_list('user_id',flat=True)
        accepted_users = set(accepted_users_all) | set(accepted_users_specific)
        users_data = [] 
        for user_id in accepted_users:
            user_profile = Userprofile.objects.get(id=user_id) 
            users_data.append({ 
                'user_id': user_profile.id, 
                'username': user_profile.username, 
                'image': user_profile.image.url if user_profile.image else None,
                'id' : user_profile.user_id
            }) 
        data = {'accepted_users': users_data}  
        
        if request.GET:
            filtered_data = ChatFilter(request.GET, queryset=Userprofile.objects.filter(id__in=accepted_users)).qs    
            serialized_data = []
            for item in filtered_data:
                serialized_data.append({
                    'user_id': item.id,
                    'username': item.username,
                    'image': item.image.url if item.image else None,
                    'id' : item.user_id
                })
            return Response(serialized_data)
        else:
            return Response(data)
        
    else: 
        user_id = user.userprofile.id 
        accepted_providers_all = PostNews.objects.filter(status='accepted', user_id=user_id).values_list('provider_id', flat=True) 
        accepted_providers_specific = PostForSpecificProviderNews.objects.filter(status='accepted',user_id=user_id).values_list('provider_id',flat=True)
        accepted_providers = set(accepted_providers_all) | set(accepted_providers_specific)
        providers_data = [] 
        for provider_id in accepted_providers: 
            provider_profile = Providerprofile.objects.get(id=provider_id) 
            providers_data.append({ 
                'provider_id': provider_profile.id, 
                'name': provider_profile.username, 
                'image': provider_profile.image.url if provider_profile.image else None,
                'id' : provider_profile.user_id,
                'phone': provider_profile.phone
            }) 
        data = {'accepted_providers': providers_data} 
        
        if request.GET:
            filtered_data = ChatFilter(request.GET, queryset=Providerprofile.objects.filter(id__in=accepted_providers)).qs    
            serialized_data = []
            for item in filtered_data:
                serialized_data.append({
                    'user_id': item.id,
                    'username': item.username,
                    'image': item.image.url if item.image else None,
                    'id' : item.user_id,
                    'phone':item.phone

                })
            return Response(serialized_data)
        else:
            return Response(data)

