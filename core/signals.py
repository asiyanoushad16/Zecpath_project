
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Candidate, Employer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == 'candidate':

            Candidate.objects.create(
                user=instance,
                full_name=instance.username
            )

        elif instance.role == 'employer':

            Employer.objects.create(
                user=instance,
                company_name='',
                location=''
            )