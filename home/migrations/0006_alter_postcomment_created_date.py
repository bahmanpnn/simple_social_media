# Generated by Django 5.0.6 on 2024-05-25 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]