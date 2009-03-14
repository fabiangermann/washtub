from wtsite.controller.models import *
from django.contrib import admin

class HostOptions(admin.ModelAdmin):
        list_display = ('name', 'ip_address', 'administrator')
             
class SettingOptions(admin.ModelAdmin):
        list_display = ('value', 'data', 'hostname')
        
admin.site.register(Host)
admin.site.register(Setting)