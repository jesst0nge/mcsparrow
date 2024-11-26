# Generated by Django 5.1.3 on 2024-11-23 02:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='quantity',
            new_name='on_hand',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='quantity',
            new_name='order_qty',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='date_last_received',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='received_quantity',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='sold_quantity',
        ),
        migrations.AddField(
            model_name='item',
            name='date_last_received',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_datercvd',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='rcvd_qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
