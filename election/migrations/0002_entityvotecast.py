# Generated by Django 2.2 on 2019-04-10 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityVotecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='election.Entity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
