# Generated by Django 3.0.5 on 2020-05-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_auto_20200502_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='pin_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_condition',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
