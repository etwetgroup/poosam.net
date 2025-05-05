from django.contrib import admin
from .models import Portfolio

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'active', 'position')
    list_filter = ('active',)
    search_fields = ('title', 'link')
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')
