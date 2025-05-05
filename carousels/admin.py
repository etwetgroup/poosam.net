from django.contrib import admin
from .models import Sliders

@admin.register(Sliders)
class SlidersAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'position', 'short_text')
    list_filter = ('active',)
    search_fields = ('title', 'short_text')
    readonly_fields = ('slug', 'm_created_date', 'sh_created_at', 'updated_date')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'image', 'short_text', 'description', 'link')
        }),
        ('وضعیت', {
            'fields': ('active', 'position')
        }),
        ('اطلاعات سیستمی', {
            'fields': ('slug', 'userId', 'm_created_date', 'sh_created_at', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
