from __future__ import unicode_literals

from persianfonts.cache import del_cached_active_font
from persianfonts.compat import force_str

from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.contrib.auth.models import Group
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Font(models.Model):
    @staticmethod
    def post_migrate_handler(**kwargs):
        del_cached_active_font()
        Font.get_active_font()

    @staticmethod
    def post_delete_handler(**kwargs):
        del_cached_active_font()
        Font.get_active_font()

    @staticmethod
    def post_save_handler(instance, **kwargs):
        del_cached_active_font()
        if instance.active:
            Font.objects.exclude(pk=instance.pk).update(active=False)
        Font.get_active_font()

    @staticmethod
    def pre_save_handler(instance, **kwargs):
        if instance.pk is None:
            try:
                obj = Font.objects.get(name=instance.name)
                if obj:
                    instance.pk = obj.pk
            except Font.DoesNotExist:
                pass

    @staticmethod
    def get_active_font():
        objs_manager = Font.objects
        objs_active_qs = objs_manager.filter(active=True)
        objs_active_ls = list(objs_active_qs)
        objs_active_count = len(objs_active_ls)

        if objs_active_count == 0:
            obj = objs_manager.all().first()
            if obj:
                obj.set_active()
            else:
                obj = objs_manager.create()

        elif objs_active_count == 1:
            obj = objs_active_ls[0]

        elif objs_active_count > 1:
            obj = objs_active_ls[-1]
            obj.set_active()

        return obj

    FONTS = (
        ('sahel', 'ساحل'),
        ('yekan', 'یکان'),
        ('parastoo', 'پرستو'),
        ('samim', 'صمیم'),
        ('shabnam', 'شبنم'),
        ('tanha', 'تنها'),
        ('vazir', 'وزیر'),
    )
    #group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="نام گروه")
    name = models.CharField(max_length=10, default='sahel', choices=FONTS, verbose_name="نوع فونت")
    active = models.BooleanField(default=True, verbose_name='وضعیت فعالیت')

    def set_active(self):
        self.active = True
        self.save()

    class Meta:
        verbose_name = "فونت"
        verbose_name_plural = "انتخاب فونت"

    def __str__(self):
        reason = dict(self.FONTS)[self.name]
        return reason


post_delete.connect(Font.post_delete_handler, sender=Font)
post_save.connect(Font.post_save_handler, sender=Font)
pre_save.connect(Font.pre_save_handler, sender=Font)
