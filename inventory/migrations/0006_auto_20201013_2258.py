# Generated by Django 3.0.2 on 2020-10-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_nostockitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nostockitems',
            name='container_name',
            field=models.CharField(choices=[('COF', 'COF'), ('TEP', 'TEP'), ('TWIN', 'TWIN'), ('ITABASHI', 'ITABASHI'), ('QP', 'QP'), ('NW', 'NW'), ('VFK', 'VFK'), ('EEL', 'EEL')], max_length=50, null=True),
        ),
    ]
