from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Providerprofile
from .models import PostForSpecificProvider, ImmediateNotification
@receiver(post_save, sender=PostForSpecificProvider)
def create_notification(sender, instance, created, **kwargs):
    if not created:
        return  

    user = instance.user
    provider = instance.provider

    if instance.accepted:
        notification_message = f"{provider.username} accepted your post."
        is_accepted_or_rejected = True
    elif instance.rejected:
        notification_message = f"{provider.username} rejected your post."
        is_accepted_or_rejected = True
    else:
        return

    existing_notification = ImmediateNotification.objects.filter(
        related_post=instance, 
        is_from_provider=is_accepted_or_rejected
    ).exists()

    if not existing_notification:
        sender = provider.user if provider.user else user

        image = instance.image if instance.image else None

        ImmediateNotification.objects.create(
            sender=sender,
            recipient=user,
            message=notification_message,
            image=image,
            is_from_provider=is_accepted_or_rejected,
            related_post=instance
        )