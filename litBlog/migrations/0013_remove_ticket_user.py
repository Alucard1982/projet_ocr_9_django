# Generated by Django 3.1.5 on 2021-01-24 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litBlog', '0012_auto_20210124_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
    ]