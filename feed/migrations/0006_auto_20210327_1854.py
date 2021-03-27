# Generated by Django 3.1.7 on 2021-03-27 18:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_post_hue'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='has_image',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator('https:\\/\\/i.imgur.com\\/\\w*.(png|jpg|gif)')]),
        ),
    ]
