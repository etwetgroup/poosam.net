from django.db import models
from django.contrib.auth.models import AbstractUser
from userauth.usermanager import UserManager

# Create your models here.
class Users(AbstractUser):
    username = None
    image = models.ImageField(max_length=200, upload_to='profiles/' , verbose_name="تصویر پروفایل")
    tel = models.CharField(max_length=255,null=True,blank=True,verbose_name="شماره ثابت")
    mobile = models.CharField(max_length=11,unique=True,verbose_name="شماره همراه")
    address = models.CharField(max_length=4000,null=True,blank=True,verbose_name="آدرس")
    gender = models.BooleanField(default=False,verbose_name="مرد / زن")
    otp = models.PositiveIntegerField(null=True,blank=True)
    otp_create_time = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    backend = 'userauth.backend.MobileBackend'