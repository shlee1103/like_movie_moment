# Generated by Django 4.2.16 on 2024-11-23 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_movies', '0006_alter_articleimage_options_remove_article_img_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articleimage',
            old_name='post',
            new_name='article',
        ),
    ]
