from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class HighScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.value, self.user)
