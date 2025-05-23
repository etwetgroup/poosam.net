# Generated by Django 5.0.7 on 2024-07-23 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('sahel', 'ساحل'), ('yekan', 'یکان'), ('parastoo', 'پرستو'), ('samim', 'صمیم'), ('shabnam', 'شبنم'), ('tanha', 'تنها'), ('vazir', 'وزیر')], default='sahel', max_length=10, verbose_name='نوع فونت')),
                ('active', models.BooleanField(default=True, verbose_name='وضعیت فعالیت')),
            ],
            options={
                'verbose_name': 'فونت',
                'verbose_name_plural': 'انتخاب فونت',
            },
        ),
    ]
