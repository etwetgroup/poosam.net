# Generated by Django 5.0.7 on 2024-07-23 15:33

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='سوال')),
                ('answer', models.CharField(max_length=4000, verbose_name='جواب')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='موقعیت')),
                ('active', models.BooleanField(default=True, verbose_name='فعالیت')),
                ('m_created_date', models.DateField(auto_now_add=True, verbose_name='تاریخ افزودن میلادی')),
                ('sh_created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن شمسی')),
                ('updated_date', models.DateField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
        ),
    ]
