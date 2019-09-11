from django.conf import settings
from django.db import models

# Create your models here.
class HighScore(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.value, self.user)
