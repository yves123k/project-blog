# Generated by Django 4.0.6 on 2022-10-13 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrossApp', '0014_remove_create_ad_number_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_ad',
            name='image',
            field=models.ImageField(upload_to='ad'),
        ),
    ]
