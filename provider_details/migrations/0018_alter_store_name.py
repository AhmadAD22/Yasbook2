# Generated by Django 5.0.1 on 2024-02-10 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_details', '0017_alter_storespecialist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=' الإسم التجاري'),
        ),
    ]
