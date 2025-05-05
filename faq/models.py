from django.db import models
from django_jalali.db import models as jmodels
from menu.models import Main

# Create your models here.
class Faq(models.Model):
    question = models.CharField(max_length=200, verbose_name="سوال")
    answer = models.CharField(max_length=4000, verbose_name="جواب")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

class Survey(models.Model):
    pages =models.ForeignKey(Main, on_delete=models.CASCADE, verbose_name="صفحه")
    full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    mobile = models.CharField(max_length=200, verbose_name="شماره تماس")
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name="ایمیل")
    description = models.CharField(max_length=4000,verbose_name="توضیحات")
    answer = models.CharField(max_length=4000, verbose_name="جواب")
    active = models.BooleanField(default=False, verbose_name="فعالیت")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")
