# Generated by Django 5.0.1 on 2024-02-11 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_login', '0010_providersubscription_promotion_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providersubscription',
            name='duration',
        ),
        migrations.AddField(
            model_name='providersubscription',
            name='duration_days',
            field=models.IntegerField(choices=[(90, '90 days'), (180, '180 days'), (365, '365 days')], default=1, verbose_name='Duration'),
            preserve_default=False,
        ),
    ]
