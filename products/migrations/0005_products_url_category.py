# Generated by Django 5.0.14 on 2025-05-05 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0019_alter_main_url_category'),
        ('products', '0004_products_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='url_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.urlcatergory', verbose_name='دسته بندی لینک'),
        ),
    ]
