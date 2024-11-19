# Generated by Django 4.2.16 on 2024-11-19 02:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_movies', '0002_remove_group_include_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='include_members',
            field=models.ManyToManyField(related_name='include_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
