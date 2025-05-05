from django.db import models
from django_jalali.db import models as jmodels
from django.utils.text import slugify
from membership.models import Users
from ckeditor_uploader.fields import RichTextUploadingField

class UrlCatergory(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    url = models.CharField(max_length=200, verbose_name='لینک')
    is_active = models.BooleanField(default=True, verbose_name="فعالیت")
    userId = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="کاربر ثبت کننده")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self) :
        return f"عنوان:{self.title} - لینک: {self.url}"


# Create your models here.
class Main(models.Model):
    sub_menu = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="زیر مجموعه")
    image = models.CharField(max_length=100, null=True, blank=True, verbose_name="عکس اصلی")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    titleseo = models.CharField(max_length=200, verbose_name="عنوان سئو")
    slug = models.SlugField(max_length=250, allow_unicode=True, null=False, editable=False)
    text = RichTextUploadingField(null=True, blank=True, verbose_name="توضیحات")
    url_category = models.ForeignKey(UrlCatergory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته بندی لینک")
    show_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='شناسه نمایش')
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    display = models.BooleanField(default=True, verbose_name="نمایش")
    showHome = models.BooleanField(default=False, verbose_name="نمایش در صفحه اصلی")
    mostVisited = models.BooleanField(default=False, verbose_name="نمایش در پربازدیدها")
    showCmnt = models.BooleanField(default=False, verbose_name="نمایش نظرات")
    keywords = models.TextField(max_length=500, null=True, blank=True, verbose_name="کلمات کلیدی")
    description = models.TextField(max_length=4000, null=True, blank=True, verbose_name="متن توضیحی")
    canonical = models.CharField(max_length=500, blank=True, verbose_name="لینک canonical")
    noindexnofollow = models.BooleanField(default=True, verbose_name="ایندکس صفحه")
    userId = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="کاربر ثبت کننده")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
