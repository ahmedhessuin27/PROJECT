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



class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = '__all__'
                
                

class GetChatNotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatNotification
        fields = ['message','id']        

                
                
                