# Generated by Django 4.0.6 on 2022-10-09 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrossApp', '0012_comments_number_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='number_comments',
        ),
        migrations.AddField(
            model_name='create_ad',
            name='number_comments',
            field=models.FloatField(default=0),
        ),
    ]
