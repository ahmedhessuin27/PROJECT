from django.db import models
from django.contrib.auth.models import User
from service.models import Service

class ChatThread(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_threads')
    is_ended = models.BooleanField(default=False)
    def __str__(self):
            return f"ChatThread {self.id}"
class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to='chat_images/', blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    additional_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True) 
    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at}"
    
