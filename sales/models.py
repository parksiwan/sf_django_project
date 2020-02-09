from django.db import models

# Create your models here.
class Sales(models.Model):
    customer = models.CharField(max_length=100, null=True)
    sales_date = models.DateField()
    product_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    product_spec = models.CharField(max_length=300, null=True)
    product_unit = models.CharField(max_length=20)
    product_cost = models.FloatField(null=True)
    product_price = models.FloatField(null=True)
    sales_qty = models.FloatField(null=True)