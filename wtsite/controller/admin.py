from wtsite.controller.models import *
from django.contrib import admin
       
class HostOptions(admin.ModelAdmin):
        list_display = ('name', 'ip_address', 'administrator')
        fieldsets = (
            (None, {'fields': ('name','ip_address','description','administrator')}),
        )

class SettingOptions(admin.ModelAdmin):
        list_display = ('value', 'data', 'hostname')
        
admin.site.register(Host)
admin.site.register(Setting)