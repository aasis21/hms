# Generated by Django 2.2 on 2019-04-10 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190410_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='block',
        ),
    ]
