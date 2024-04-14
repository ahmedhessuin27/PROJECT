from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification,Providerprofile
from notification.models import Post,PostNews


@receiver(post_save, sender=Post)
def create_notification(sender, instance, created, **kwargs):
    if created :
        service_providers = Providerprofile.objects.filter(profession=instance.service,city=instance.city)
        for provider in service_providers:
            Notification.objects.create(
            recipient1=provider,
            message=f'A new post has been added in your service by {instance.user.username}',
            post = instance
            
        )
            
            
            
@receiver(post_save, sender=PostNews)
def send_notification_on_post_accept(sender, instance, created, **kwargs):
    if created :
        Notification.objects.create(
            recipient2=instance.user,
            message=f'Your post has been accepted by {instance.provider.username}',
            post = instance.post
        )
        
        