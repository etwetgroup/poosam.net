from django.db import models
from django_jalali.db import models as jmodels
from django.utils.text import slugify
from membership.models import Users

class Sliders(models.Model):
    # type = models.CharField(max_length=50, verbose_name="نوع اسلایدر")
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="عنوان")
    slug = models.SlugField(max_length=250, allow_unicode=True, null=False, editable=False)
    image = models.ImageField(max_length=100, null=True, blank=True, upload_to='carousels/main/', verbose_name="عکس")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name="لینک")
    short_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="متن کوتاه")
    description = models.CharField(max_length=400, null=True, blank=True, verbose_name="توضیحات")
    # view_in = models.IntegerField(default=0, verbose_name="مشاهده در")
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