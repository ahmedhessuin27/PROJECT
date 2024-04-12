from django.db import models
from django.contrib.auth.models import User
from service.models import Service
from account.models import Providerprofile , Userprofile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # يستخرج الامتداد من اسم الملف
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Only JPG and PNG are allowed.'))


class ChatThread(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_threads')
    is_ended = models.BooleanField(default=False)
    def __str__(self):
            return f"ChatThread {self.id}"
class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)






class Post(models.Model): 
    CITIES_CHOICES = ( 
        ('Cairo', 'Cairo'), 
        ('Alexandria', 'Alexandria'), 
        ('Giza', 'Giza'), 
        ('Luxor', 'Luxor'), 
        ('Aswan', 'Aswan'), 
        ('Damietta', 'Damietta'), 
        ('Port Said', 'Port Said'), 
        ('Suez', 'Suez'), 
        ('Ismailia', 'Ismailia'), 
        ('Faiyum', 'Faiyum'), 
        ('Beni Suef', 'Beni Suef'), 
        ('Minya', 'Minya'), 
        ('Assiut', 'Assiut'), 
        ('Sohag', 'Sohag'), 
        ('Qena', 'Qena'), 
        ('Red Sea', 'Red Sea'), 
        ('New Valley', 'New Valley'), 
        ('Matrouh', 'Matrouh'), 
        ('Kafr El Sheikh', 'Kafr El Sheikh'), 
        ('Monufia', 'Monufia'), 
        ('Dakahlia', 'Dakahlia'), 
        ('Sharqia', 'Sharqia'), 
        ('North Sinai', 'North Sinai'), 
        ('South Sinai', 'South Sinai'), 
        ('Beheira', 'Beheira'), 
        ('Gharbia', 'Gharbia'), 
        ('Qalyubia', 'Qalyubia'), 
    ) 
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE) 
    problem_description = models.TextField() 
    service = models.ForeignKey(Service, on_delete=models.CASCADE) 
    service_name = models.CharField(max_length=20, blank=True,null=True) 
    city = models.CharField(max_length=20,choices=CITIES_CHOICES,null=False,blank=False) 
    created_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to='post_images/', blank=True , null=True,validators=[validate_image_extension])  
    def str(self): 
        return f"Post by {self.user.username} - {self.created_at}"
    


class PostNews(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    provider = models.ForeignKey(Providerprofile,on_delete=models.CASCADE,null=True,blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']        



class PostForSpecificProvider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Providerprofile, on_delete=models.CASCADE, related_name='provider_posts')
    message = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def str(self):
        return f"Post by {self.user.username} for {self.provider.username}"

   
class ImmediateNotification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.TextField()
    image = models.ImageField(upload_to='notification_images/', blank=True, null=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    is_from_provider = models.BooleanField(default=False)
    related_post = models.ForeignKey(PostForSpecificProvider, on_delete=models.CASCADE, blank=True, null=True)        













