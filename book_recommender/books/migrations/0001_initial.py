# Generated by Django 5.2 on 2025-05-11 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('original_price', models.CharField(blank=True, max_length=255, null=True)),
                ('discount', models.CharField(blank=True, max_length=255, null=True)),
                ('discount_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=255, null=True)),
                ('images_url', models.TextField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, max_length=255, null=True)),
                ('review_count', models.CharField(blank=True, max_length=255, null=True)),
                ('inventory_status', models.CharField(blank=True, max_length=255, null=True)),
                ('inventory_type', models.CharField(blank=True, max_length=255, null=True)),
                ('sold_quantity', models.CharField(blank=True, max_length=255, null=True)),
                ('current_seller_name', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('book_cover', models.CharField(blank=True, max_length=255, null=True)),
                ('number_of_page', models.CharField(blank=True, max_length=255, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
    ]
