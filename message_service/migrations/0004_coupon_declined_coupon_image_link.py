# Generated by Django 3.1.7 on 2023-10-01 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_service', '0003_auto_20230930_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='declined_coupon_image_link',
            field=models.CharField(default='123', max_length=300),
        ),
    ]
