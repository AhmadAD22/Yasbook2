# Generated by Django 5.0.1 on 2024-04-08 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_login', '0016_alter_providersubscription_duration_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/provider/store/', verbose_name='رفع الصورة')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_login.provider')),
            ],
        ),
    ]
