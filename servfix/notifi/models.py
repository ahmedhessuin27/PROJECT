
from django.db import models
from django.contrib.auth.models import User

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

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    additional_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True)  # New field for the image
    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at}"
    
