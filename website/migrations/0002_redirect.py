# Generated by Django 5.0.4 on 2024-08-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_url', models.CharField(max_length=4000)),
                ('new_url', models.CharField(max_length=4000)),
            ],
        ),
    ]
