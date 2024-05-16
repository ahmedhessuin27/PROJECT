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

# class PostSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = Post 
#         fields = ['problem_description','image','service_name','city','id']
class PostSerializer(serializers.ModelSerializer): 
    is_accepted = serializers.SerializerMethodField() 
 
    class Meta: 
        model = Post 
        fields = ['problem_description', 'image', 'service_name', 'city', 'is_accepted'] 
 
    def get_is_accepted(self, obj): 
        try: 
            post_news_obj = PostNews.objects.get(post_id=obj.id) 
            return post_news_obj.status == 'accepted' 
        except PostNews.DoesNotExist: 
            return False
        
        
        
        
class PostNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNews
        fields = '__all__'
        

class RelatedAcceptedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['problem_description','image','city','id','service_name']


class RelatedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostForSpecificProvider
        fields = ['message','image','id']

        
class AcceptedPostsSerializer(serializers.ModelSerializer):
    post_details = RelatedAcceptedPostsSerializer(source='post',read_only=True)
    
    class Meta:
        model = PostNews
        fields = ['post_details',]
     

# class PostForSpecificProviderSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = PostForSpecificProvider 
#         fields = ['id', 'user', 'provider', 'message', 'image', 'created_at'] 
#         read_only_fields = ['created_at'] 
class PostForSpecificProviderSerializer(serializers.ModelSerializer): 
    is_accepted = serializers.SerializerMethodField() 
 
    class Meta: 
        model = PostForSpecificProvider 
        fields = ['id', 'user', 'provider', 'message', 'image', 'created_at', 'is_accepted'] 
        read_only_fields = ['created_at', 'is_accepted'] 
 
    def get_is_accepted(self, obj): 
        try: 
            provider_news_posts = PostForSpecificProviderNews.objects.filter(post_id=obj.id) 
            if provider_news_posts.exists(): 
                latest_status = provider_news_posts.last().status 
                return latest_status == 'accepted' 
            else: 
                return False 
        except PostForSpecificProviderNews.DoesNotExist: 
            return False
 
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
        fields ='__all__'        

