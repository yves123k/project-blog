# Generated by Django 4.0.6 on 2022-10-08 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CrossApp', '0004_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_ad',
            name='comment_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_author', to='CrossApp.comments'),
        ),
    ]
