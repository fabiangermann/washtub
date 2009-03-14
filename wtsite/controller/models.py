from django.db import models

# Create your models here.
class Setting(models.Model):
    value = models.CharField(max_length=128)
    data = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    
    class Admin:
        pass


