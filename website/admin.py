from django.contrib import admin
from .models import Config, Redirect

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'link')
    search_fields = ('key', 'value')

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_url', 'new_url')
    search_fields = ('old_url', 'new_url')
