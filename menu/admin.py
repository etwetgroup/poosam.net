from django.contrib import admin
from .models import Main, UrlCatergory

@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_menu', 'active', 'display', 'position', 'url_category', 'show_id')
    list_filter = ('active', 'display', 'showHome', 'mostVisited', 'showCmnt', 'url_category')
    search_fields = ('title', 'titleseo', 'description')
    readonly_fields = ('slug', 'm_created_date', 'sh_created_at', 'updated_date')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('sub_menu', 'title', 'titleseo', 'text', 'image')
        }),
        ('SEO', {
            'fields': ('keywords', 'description', 'canonical', 'noindexnofollow'),
            'classes': ('collapse',)
        }),
        ('نمایش', {
            'fields': ('active', 'display', 'showHome', 'mostVisited', 'showCmnt', 'position')
        }),
        ('لینک', {
            'fields': ('url_category', 'show_id')
        }),
        ('اطلاعات سیستمی', {
            'fields': ('slug', 'userId', 'm_created_date', 'sh_created_at', 'updated_date'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UrlCatergory)
class UrlCatergoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'url')
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')
