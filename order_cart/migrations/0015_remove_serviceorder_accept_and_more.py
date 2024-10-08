# Generated by Django 5.0.1 on 2024-07-18 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_cart', '0014_remove_productorder_accept_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='accept',
        ),
        migrations.RemoveField(
            model_name='serviceorder',
            name='accomplished',
        ),
        migrations.RemoveField(
            model_name='serviceorder',
            name='canceled',
        ),
        migrations.RemoveField(
            model_name='serviceorder',
            name='rejected',
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
