# Generated by Django 5.0.1 on 2024-09-21 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_login', '0029_myuser_fcm_token'),
        ('order_cart', '0019_productorder_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('titleArgs', models.JSONField(default=list)),
                ('body', models.TextField()),
                ('bodyArgs', models.JSONField(default=list)),
                ('sentAt', models.DateTimeField(auto_now_add=True)),
                ('localized', models.BooleanField(default=True)),
                ('product_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order_cart.productorder')),
                ('service_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order_cart.serviceorder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sentAt'],
            },
        ),
    ]
