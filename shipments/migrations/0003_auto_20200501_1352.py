# Generated by Django 3.0.5 on 2020-05-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_auto_20200501_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerdetails',
            name='client_secret',
            field=models.CharField(max_length=100),
        ),
    ]