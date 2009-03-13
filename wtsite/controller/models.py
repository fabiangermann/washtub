from django.db import models

# Create your models here.
class Setting(models.Model):
    value = models.CharField(max_length=128)
    data = models.CharField()
    hostname = models.CharField(max_length=255)
