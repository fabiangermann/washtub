from django.db import models

# Create your models here.
class Setting(models.Model):
    value = CharField(max_length=128)
    data = CharField()
    hostname = CharField(max_length=255)
