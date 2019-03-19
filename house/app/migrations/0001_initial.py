# Generated by Django 2.1.1 on 2019-03-19 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('house_type', models.CharField(max_length=32)),
                ('floor', models.CharField(max_length=32)),
                ('coverArea', models.DecimalField(decimal_places=2, max_digits=12)),
                ('house_struct', models.CharField(max_length=32)),
                ('inside_area', models.CharField(max_length=32)),
                ('build_type', models.CharField(max_length=32)),
                ('orientation', models.CharField(max_length=32)),
                ('build_struct', models.CharField(max_length=32)),
                ('redecorated', models.CharField(max_length=32)),
                ('ladder_household_ratio', models.CharField(max_length=32)),
                ('heating_mode', models.CharField(max_length=32)),
                ('is_elevator', models.CharField(max_length=32)),
                ('property', models.CharField(max_length=32)),
                ('use_water_type', models.CharField(max_length=32)),
                ('electricity_type', models.CharField(max_length=32)),
                ('listing_date', models.DateField()),
                ('trade_right', models.CharField(max_length=32)),
                ('last_transaction', models.DateField()),
                ('house_use', models.CharField(max_length=32)),
                ('house_years', models.CharField(max_length=32)),
                ('property_owner', models.CharField(max_length=32)),
                ('mortgage_info', models.CharField(max_length=32)),
                ('spare_parts', models.CharField(max_length=32)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('square_metre_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('district', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('area', models.CharField(max_length=32)),
                ('street', models.CharField(max_length=32)),
            ],
        ),
    ]
