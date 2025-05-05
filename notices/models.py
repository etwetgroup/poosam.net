from django.db import models
from django_jalali.db import models as jmodels
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from membership.models import Users
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Category(models.Model):
    image = models.ImageField(max_length=100, null=True, blank=True, upload_to='uploads/notices/', verbose_name="عکس")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    titleseo = models.CharField(max_length=200, verbose_name="عنوان سئو")
    slug = models.SlugField(max_length=250, allow_unicode=True, null=False, editable=False)
    keywords = models.CharField(max_length=500, null=True, blank=True, verbose_name="کلمات کلیدی")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="متن توضیحی")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")
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


class News(models.Model):
    newscat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="گروه")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    titleseo = models.CharField(max_length=200, verbose_name="عنوان سئو")
    slug = models.SlugField(max_length=250, allow_unicode=True, null=False, editable=False)
    short_text = models.TextField(max_length=200, verbose_name="متن کوتاه")
    text = RichTextUploadingField(null=True, blank=True, verbose_name="توضیحات")
    active = models.BooleanField(default=True, verbose_name="فعالیت")
    hot = models.BooleanField(default=False, verbose_name="ویژه")
    image = models.ImageField(max_length=100, null=True, blank=True, upload_to='uploads/notices/', verbose_name="عکس")
    keywords = models.CharField(max_length=4000, null=True, blank=True, verbose_name="کلمات کلیدی")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="متن توضیحی")
    view_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="تعداد بازدید")
    m_created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ افزودن میلادی")
    sh_created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن شمسی")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title