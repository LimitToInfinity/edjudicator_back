from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return "{} - {}".format(self.username, self.email)

class HighScore(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    value = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_high_score(sender, instance, created, **kwargs):
        if created:
            HighScore.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_high_score(sender, instance, **kwargs):
        instance.high_score.save()

    def __str__(self):
        return "{} - {}".format(self.value, self.user)
