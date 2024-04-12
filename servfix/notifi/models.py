from django.db import models
from django.contrib.auth.models import User 
from account.models import Providerprofile , Userprofile


class Notification(models.Model):
    recipient1 = models.ForeignKey(Providerprofile, on_delete=models.CASCADE, null=True, blank=True)
    recipient2 = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.recipient1.username}: {self.message}"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    