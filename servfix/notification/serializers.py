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
        fields = '__all__'
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmediateNotification
        fields = '__all__'        
        
             