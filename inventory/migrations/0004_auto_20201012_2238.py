# Generated by Django 3.0.2 on 2020-10-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20201012_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adailyusage',
            name='cust_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='usage',
            name='cust_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
