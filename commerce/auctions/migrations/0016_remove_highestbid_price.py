# Generated by Django 3.2.8 on 2021-12-15 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_highestbid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highestbid',
            name='price',
        ),
    ]
