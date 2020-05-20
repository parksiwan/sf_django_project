# Generated by Django 3.0.2 on 2020-05-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_dailystock_dailyusage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageTransactLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transact_date', models.DateField()),
                ('transact_time', models.TimeField()),
                ('storage_loc', models.CharField(max_length=10, null=True)),
                ('transact_type', models.CharField(max_length=20)),
                ('pallet_qty', models.FloatField(null=True)),
                ('total_pallet_after_transaction', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'Storage Transaction Log',
                'verbose_name_plural': 'Storage Transaction Logs',
            },
        ),
        migrations.RenameModel(
            old_name='DailyStock',
            new_name='aDailyStock',
        ),
        migrations.RenameModel(
            old_name='DailyUsage',
            new_name='aDailyUsage',
        ),
        migrations.AlterModelOptions(
            name='adailystock',
            options={'verbose_name': 'Daily Stock', 'verbose_name_plural': 'Daily Stocks'},
        ),
        migrations.AlterModelOptions(
            name='adailyusage',
            options={'verbose_name': 'Daily Usage', 'verbose_name_plural': 'Daily Usages'},
        ),
        migrations.AlterModelOptions(
            name='currentstock',
            options={'verbose_name': 'Main Aggregated Stock', 'verbose_name_plural': 'Main Aggregated Stocks'},
        ),
        migrations.AlterModelOptions(
            name='monthlyusage',
            options={'verbose_name': 'Main Monthly Usage', 'verbose_name_plural': 'Main Monthly Usages'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Main Stock', 'verbose_name_plural': 'Main Stocks'},
        ),
        migrations.AlterModelOptions(
            name='usage',
            options={'verbose_name': 'Main Usage', 'verbose_name_plural': 'Main Usages'},
        ),
    ]