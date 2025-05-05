from django.db import models

# Create your models here.
class Config(models.Model):
    key = models.CharField(max_length=250 , blank=False, null=False , verbose_name="کلید")
    value = models.CharField(max_length=4000, blank=False, null=False, verbose_name="توضیحات")
    link = models.CharField(max_length=250 , blank=False, null=False , verbose_name="لینک")


class Redirect(models.Model):
    old_url = models.CharField(max_length=4000 , blank=False, null=False)
    new_url = models.CharField(max_length=4000, blank=False, null=False)    
