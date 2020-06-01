from django.db import models

# Create your models here.
class MonthlyUsage(models.Model):
    usage_month = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    customer = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    plenus_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)#, choices=unit_choices)    

    class Meta:
        verbose_name = "Plenus Monthly Usage"
        verbose_name_plural = "Plenus Monthly Usages"


class Stock(models.Model):
    stock_base_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)    
    plenus_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    qty = models.FloatField()    
    unit = models.CharField(max_length=20)
    bbd = models.DateField(null=True)
            
    class Meta:
        verbose_name = "Plenus Stock"
        verbose_name_plural = "Plenus Stocks"