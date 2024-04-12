from rest_framework import serializers
from .models import *

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatThread
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Post 
        fields = ['problem_description','image','service_name','city']
        
        
        
        
class PostNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNews
        fields = '__all__'
        

class RelatedAcceptedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['problem_description','image']

        
class AcceptedPostsSerializer(serializers.ModelSerializer):
    post_details = RelatedAcceptedPostsSerializer(source='post',read_only=True)
    
    class Meta:
        model = PostNews
        fields = ['post_details',]
     

class PostForSpecificProviderSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PostForSpecificProvider 
        fields = ['id', 'user', 'provider', 'message', 'image', 'created_at', 'accepted', 'rejected'] 
        read_only_fields = ['accepted', 'rejected']  # Mark these fields as read-only 
 
 
class ImmediateNotificationSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ImmediateNotification 
        fields = ['id', 'sender', 'recipient', 'message', 'image', 'created_at', 'is_from_provider', 'related_post'] 
 
class NotificationDeleteSerializer(serializers.Serializer): 
    pass
             