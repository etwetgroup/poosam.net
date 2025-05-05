from django.contrib import admin
from .models import Faq, Survey

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'active', 'position')
    list_filter = ('active',)
    search_fields = ('question', 'answer')
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile', 'pages', 'active')
    list_filter = ('active', 'pages')
    search_fields = ('full_name', 'mobile', 'email')
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')
