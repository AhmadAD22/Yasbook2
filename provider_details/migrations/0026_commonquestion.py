# Generated by Django 5.0.1 on 2024-07-17 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_details', '0025_store_whatsapp_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاريخ الإنشاء')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='تاريخ التحديث')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storeCommonQuestion', to='provider_details.store')),
            ],
        ),
    ]
