# Generated by Django 3.1.5 on 2021-01-21 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litLogin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
