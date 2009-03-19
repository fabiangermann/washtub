from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Host(models.Model):
    name = models.CharField(max_length=128)
    ip_address = models.IPAddressField('Server IP Address')
    description = models.TextField('Description', blank=True)
    admin_group = models.ManyToManyField(Group, related_name='host_admin_group', blank=True)
    admin = models.ForeignKey(User, related_name='host_admin', default=1)

    def __unicode__(self):
    	return self.name
    
class Setting(models.Model):
    SETTINGS_CHOICES = (
    	('port', 'Port'),
    	('protocol', 'Protocol'),
    	)

    value = models.CharField(max_length=128, choices=SETTINGS_CHOICES)
    data = models.CharField(max_length=255)
    hostname = models.ForeignKey('Host',default=1)
    
    def __unicode__(self):
        return self.data
    
    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
