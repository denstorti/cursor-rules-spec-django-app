from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, FreelancerProfile, HirerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a profile when a user is created.
    This is a backup in case the profile was not created during registration.
    """
    if created:
        # Only create profiles if they don't already exist
        if instance.is_freelancer and not hasattr(instance, 'freelancer_profile'):
            try:
                FreelancerProfile.objects.get(user=instance)
            except FreelancerProfile.DoesNotExist:
                FreelancerProfile.objects.create(user=instance)
        
        elif instance.is_hirer and not hasattr(instance, 'hirer_profile'):
            try:
                HirerProfile.objects.get(user=instance)
            except HirerProfile.DoesNotExist:
                HirerProfile.objects.create(user=instance) 