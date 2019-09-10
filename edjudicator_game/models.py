from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HighScore(models.Model):
    value = models.IntegerField(null=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return "{} - {}".format(self.value, self.user)
    def __str__(self):
        return "{}".format(self.value)