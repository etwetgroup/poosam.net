from django.contrib import admin
from .models import Products, DetailsTitle, Details

class DetailsInline(admin.TabularInline):
    model = Details
    extra = 1

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pages', 'price', 'active', 'position', 'show_id', 'url_category')
    list_filter = ('active', 'pages', 'url_category')
    search_fields = ('title', 'show_id')
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')
    inlines = [DetailsInline]

@admin.register(DetailsTitle)
class DetailsTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pages', 'active', 'position')
    list_filter = ('active', 'pages')
    search_fields = ('title',)
    readonly_fields = ('m_created_date', 'sh_created_at', 'updated_date')
