from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class HighScore(models.Model):
    user = models.ForeignKey(get_user_model(), db_column="user", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.value, self.user)
