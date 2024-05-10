from django.db import models
from django.contrib.auth.models import User

class ChatRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    service_provider_accepted = models.BooleanField(default=False)
    client_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


