from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Job


@receiver(post_save, sender=Job)
def check_job_expiration(sender, instance, created, **kwargs):
    """
    Check if a job has expired and update its status if needed
    """
    if not created and instance.status == Job.Status.PUBLISHED:
        # Check if job has passed deadline
        if instance.is_expired:
            instance.status = Job.Status.EXPIRED
            instance.save(update_fields=["status"]) 