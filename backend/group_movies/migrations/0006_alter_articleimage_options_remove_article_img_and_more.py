# Generated by Django 4.2.16 on 2024-11-23 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_movies', '0005_remove_article_like_users_remove_article_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleimage',
            options={},
        ),
        migrations.RemoveField(
            model_name='article',
            name='img',
        ),
        migrations.RemoveField(
            model_name='articleimage',
            name='order',
        ),
    ]
