from wtsite.controller.models import *
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
	list_display = ('name', 'ip_address')

class SettingAdmin(admin.ModelAdmin):
	list_filter = ['hostname']
	list_display = ('value', 'data', 'hostname')

admin.site.register(Host, HostAdmin)
admin.site.register(Setting, SettingAdmin)
