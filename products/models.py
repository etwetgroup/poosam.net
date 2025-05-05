from django.db import models
from django_jalali.db import models as jmodels
from menu.models import Main, UrlCatergory
# Create your models here.
class DetailsTitle(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    pages = models.ForeignKey(Main, on_delete=models.CASCADE, verbose_name="زیر مجموعه")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.title

class Products(models.Model):
    image = models.ImageField(max_length=100, null=True, blank=True, upload_to='uploads/products/', verbose_name="عکس")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    pages = models.ForeignKey(Main, on_delete=models.CASCADE, verbose_name="دسته بندی")
    product = models.IntegerField(verbose_name="زیر مجموعه")
    price = models.CharField(max_length=20, verbose_name="قیمت")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    url_category = models.ForeignKey(UrlCatergory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته بندی لینک")
    show_id = models.CharField(max_length=200, unique=True,verbose_name='شناسه نمایش')
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.title

class Details(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    detail = models.ForeignKey(DetailsTitle, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)