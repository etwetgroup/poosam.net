# Generated by Django 5.0.7 on 2024-07-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/pages/', verbose_name='عکس'),
        ),
    ]
