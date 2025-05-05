from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Font


class FontAdmin(admin.ModelAdmin):
    #list_display = ('group','name')
    list_display = ('name',)
    exclude = ('active',)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #
    #     if request.user.is_superuser:
    #         return qs
    #
    #     list_of_ids = []
    #     for g in request.user.groups.all():
    #         list_of_ids.append(g.id)
    #
    #     return qs.filter(group_id__in=list_of_ids)

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    # def get_model_perms(self, request):
    #     if request.user.is_superuser:
    #         return {}
    #     return super(FontAdmin, self).get_model_perms(request)

admin.site.register(Font, FontAdmin)
