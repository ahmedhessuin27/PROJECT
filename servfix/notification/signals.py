from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User

from account.models import Providerprofile
from .models import PostForSpecificProvider, ImmediateNotification
@receiver(post_save, sender=User) 
def create_provider_profile(sender, instance, created, **kwargs): 
    if created: 
        Providerprofile.objects.create(user=instance)
        