from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
class Portfolio(models.Model):
    image = models.ImageField(max_length=100, null=True, blank=True, upload_to='uploads/portfolio/', verbose_name="عکس")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    link = models.CharField(max_length=200, verbose_name="لینک")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
