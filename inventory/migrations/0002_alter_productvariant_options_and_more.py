# Generated by Django 5.1.3 on 2024-11-22 16:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productvariant',
            options={'get_latest_by': 'date_last_received'},
        ),
        migrations.AddField(
            model_name='productvariant',
            name='date_last_received',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]