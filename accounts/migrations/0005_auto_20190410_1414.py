# Generated by Django 2.1.7 on 2019-04-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190409_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='block',
            field=models.CharField(default='None', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='branch',
            field=models.CharField(default='None', max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='program',
            field=models.CharField(default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(default='None', max_length=255),
        ),
    ]