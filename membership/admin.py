from django.contrib import admin
from membership.models import *

# Register your models here.
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('mobile','first_name','last_name','is_active')
    list_filter = ('is_active',)
    ordering = ['-id']
    search_fields = ['mobile','first_name','last_name','email']
    exclude = ['otp',]

admin.site.register(Users,MembershipAdmin)