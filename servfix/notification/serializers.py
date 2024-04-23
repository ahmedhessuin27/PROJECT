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
        fields = ['problem_description','image','service_name','city','id']
        
        
        
        
class PostNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNews
        fields = '__all__'
        

class RelatedAcceptedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['problem_description','image','city','id','service_name']

        
class AcceptedPostsSerializer(serializers.ModelSerializer):
    post_details = RelatedAcceptedPostsSerializer(source='post',read_only=True)
    
    class Meta:
        model = PostNews
        fields = ['post_details',]
     

class PostForSpecificProviderSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PostForSpecificProvider 
        fields = ['id', 'user', 'provider', 'message', 'image', 'created_at'] 
        read_only_fields = ['created_at'] 
 
class ImmediateNotificationSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ImmediateNotification 
        fields = ['id', 'user_recipient', 'provider_recipient', 'message', 'image', 'created_at', 'post'] 
        read_only_fields = ['created_at'] 
         
         
class PostForSpecificProviderNewsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PostForSpecificProviderNews 
        fields = '__all__' 
       
             
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ['sender','recipient','content','timestamp']             





class AcceptedUsersSerializer(serializers.Serializer): 
    user_id = serializers.IntegerField() 
    username = serializers.CharField() 
    image = serializers.ImageField() 
 
class AcceptedProvidersSerializer(serializers.Serializer): 
    provider_id = serializers.IntegerField() 
    name = serializers.CharField() 
    image = serializers.ImageField()
     
     
class NotificationSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ImmediateNotification 
        fields = ['post_id', 'message']        

