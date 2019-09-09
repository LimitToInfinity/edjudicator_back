from django.db import models

# Create your models here.
class HighScore(models.Model):
    value = models.IntegerField(null=False)

    def __str__(self):
        return "{}".format(self.value)