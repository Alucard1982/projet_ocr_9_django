# Generated by Django 3.1.5 on 2021-01-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litBlog', '0003_auto_20210121_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192),
        ),
    ]