# Generated by Django 5.0.1 on 2024-02-15 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_cart', '0004_alter_servicecartitem_duration_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicecartitem',
            options={'verbose_name': 'Service Cart Item', 'verbose_name_plural': 'Service Cart Items'},
        ),
        migrations.RemoveField(
            model_name='servicecartitem',
            name='duration',
        ),
        migrations.AddField(
            model_name='servicecartitem',
            name='duration_minutes',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='مدة الخدمة (بالدقائق)'),
        ),
    ]
