from django.contrib import admin
from .models import Category, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'position')
    list_filter = ('active',)
    search_fields = ('title', 'titleseo', 'description', 'keywords')
    readonly_fields = ('slug', 'm_created_date', 'sh_created_at', 'updated_date')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'titleseo', 'image')
        }),
        ('SEO', {
            'fields': ('keywords', 'description'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('active', 'position')
        }),
        ('اطلاعات سیستمی', {
            'fields': ('slug', 'userId', 'm_created_date', 'sh_created_at', 'updated_date'),
            'classes': ('collapse',)
        }),
    )

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'newscat', 'active', 'hot', 'view_count')
    list_filter = ('active', 'hot', 'newscat')
    search_fields = ('title', 'titleseo', 'short_text', 'keywords', 'description')
    readonly_fields = ('slug', 'm_created_date', 'sh_created_at', 'updated_date', 'view_count')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('newscat', 'title', 'titleseo', 'short_text', 'text', 'image')
        }),
        ('SEO', {
            'fields': ('keywords', 'description'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('active', 'hot')
        }),
        ('اطلاعات سیستمی', {
            'fields': ('slug', 'view_count', 'm_created_date', 'sh_created_at', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
