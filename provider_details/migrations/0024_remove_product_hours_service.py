# Generated by Django 5.0.1 on 2024-07-16 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_details', '0023_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hours_Service',
        ),
    ]
