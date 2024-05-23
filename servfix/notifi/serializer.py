from rest_framework import serializers
from .models import Notification , ChatMessages , ChatNotification

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        
        
        
class RelatedChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ['content',]


                
                

class GetChatNotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatNotification
        fields = ['message','id'] 


class ChatMessagesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    unseen_messages = serializers.CharField()
    
    class Meta:
        model = ChatMessages
        fields = ['content','name','unseen_messages']  


class ChatMessagesForSpecificPersonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatMessages
        fields = ['content','sender','recipient','timestamp']

        

                
                
                