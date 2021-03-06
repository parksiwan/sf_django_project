# Generated by Django 3.0.2 on 2020-07-26 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_month', models.DateField()),
                ('product_type', models.CharField(max_length=10, null=True)),
                ('customer', models.CharField(max_length=40, null=True)),
                ('sf_code', models.CharField(max_length=20)),
                ('plenus_code', models.CharField(max_length=20)),
                ('product_name', models.CharField(max_length=300, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('qty', models.FloatField(null=True)),
                ('unit', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Plenus Monthly Usage',
                'verbose_name_plural': 'Plenus Monthly Usages',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_base_date', models.DateField()),
                ('product_type', models.CharField(max_length=10, null=True)),
                ('sf_code', models.CharField(max_length=20)),
                ('plenus_code', models.CharField(max_length=20)),
                ('product_name', models.CharField(max_length=300, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('qty', models.FloatField()),
                ('unit', models.CharField(max_length=20)),
                ('bbd', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Plenus Stock',
                'verbose_name_plural': 'Plenus Stocks',
            },
        ),
    ]
