from django.db import models

# Create your models here.
class PackingList(models.Model):
    dispatch_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    customer = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)#, choices=unit_choices)
    arrival_date = models.DateField(null=True)