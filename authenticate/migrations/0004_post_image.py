# Generated by Django 4.1.7 on 2023-03-09 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0003_finance'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='img/%y'),
        ),
    ]
