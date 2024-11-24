# Generated by Django 4.2.16 on 2024-11-24 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_movies', '0002_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('poster_path', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
