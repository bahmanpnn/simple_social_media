# Generated by Django 5.0.6 on 2024-05-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_posts_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]