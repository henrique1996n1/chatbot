# Generated by Django 3.1.7 on 2023-09-30 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_service', '0002_auto_20230930_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionalmessage',
            name='answer',
            field=models.CharField(choices=[('D', 'Declined'), ('NA', 'Not Answered'), ('A', 'Accepted')], default='NA', max_length=2),
        ),
    ]
