from django.db import models
from django.contrib.auth.models import User 
from account.models import Providerprofile , Userprofile
from notification.models import Post , ChatMessages



class Notification(models.Model):
    recipient1 = models.ForeignKey(Providerprofile, on_delete=models.CASCADE, null=True, blank=True)
    recipient2 = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=10,default='type 1',null=True)


    def __str__(self):
        return f"{self.recipient1.username}: {self.message}"
    
    
    
    
class ChatNotification(models.Model):
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    content = models.ForeignKey(ChatMessages,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   
         
    def str(self):
        return f"{self.recipient.username}: {self.message}"    
    
    
    
    
    
    
    
    
    
    