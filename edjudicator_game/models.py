from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

# Create your models here.
class HighScore(models.Model):
    user = models.OneToOneField(
         User,
         on_delete=models.CASCADE,
         primary_key=True,
    )
    value = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        HighScore.objects.create(user=instance)
