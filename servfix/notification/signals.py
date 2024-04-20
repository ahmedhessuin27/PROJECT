from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User

from account.models import Providerprofile
from .models import PostForSpecificProvider, ImmediateNotification, PostForSpecificProviderNews
@receiver(post_save, sender=User) 
def create_provider_profile(sender, instance, created, **kwargs): 
    if created: 
        Providerprofile.objects.create(user=instance)


@receiver(post_save, sender=PostForSpecificProvider) 
def create_immediate_notification_for_post(sender, instance, created, **kwargs): 
    if created: 
        notification_message = f"New post sent to you by {instance.user.username}" 
        ImmediateNotification.objects.create( 
            user_recipient=instance.provider.user, 
            message=notification_message, 
            image=instance.image, 
            post=instance 
        ) 
 
# Signal handler for creating immediate notification when a post news is created 
@receiver(post_save, sender=PostForSpecificProviderNews) 
def create_immediate_notification_for_news(sender, instance, created, **kwargs): 
    if created and instance.status == 'accepted': 
        message = f"{instance.provider.user.username} accepted your post." 
        ImmediateNotification.objects.create( 
            user_recipient=instance.user.userprofile, 
            provider_recipient=instance.provider, 
            message=message, 
            post=instance.post 
        ) 
 
    elif created and instance.status == 'rejected': 
        message = f"{instance.provider.user.username} rejected your post." 
        ImmediateNotification.objects.create( 
            user_recipient=instance.user.userprofile, 
            provider_recipient=instance.provider, 
            message=message, 
            post=instance.post 
        )        



        