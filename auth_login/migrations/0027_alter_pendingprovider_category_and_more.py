# Generated by Django 5.0.1 on 2024-06-07 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_login', '0026_alter_pendingprovider_otp'),
        ('categroy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingprovider',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categroy.category'),
        ),
        migrations.AlterField(
            model_name='pendingprovider',
            name='otp',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pendingProvider', to='auth_login.otprequest'),
        ),
    ]
