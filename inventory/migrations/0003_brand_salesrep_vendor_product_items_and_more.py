# Generated by Django 5.1.3 on 2024-11-23 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_rename_quantity_item_on_hand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('b2b', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesRep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='product_variants', to='inventory.item'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='barcode',
            field=models.ImageField(default='', upload_to='uploads/product/'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='details',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productvariant',
            name='lightspeedid',
            field=models.IntegerField(default=1, max_length=13),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='sparrownumber',
            field=models.CharField(default=1, max_length=12),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='upc',
            field=models.IntegerField(default=1, max_length=12),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('barcode', models.CharField(max_length=50)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='inventory.brand')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='inventory.product')),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='rep',
            field=models.ManyToManyField(blank=True, related_name='rep', to='inventory.salesrep'),
        ),
        migrations.CreateModel(
            name='SubCategory1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sub_category1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.subcategory1')),
            ],
        ),
        migrations.AddField(
            model_name='salesrep',
            name='vendor',
            field=models.ManyToManyField(blank=True, related_name='vendor', to='inventory.vendor'),
        ),
        migrations.AddField(
            model_name='brand',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor'),
        ),
    ]