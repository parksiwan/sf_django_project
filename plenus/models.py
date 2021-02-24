from django.db import models

# Create your models here.
class MonthlyUsage(models.Model):
    usage_month = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    customer = models.CharField(max_length=40, null=True)
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


class CKStock(models.Model):
    transact_type_choices = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),
    )
    transact_type = models.CharField(max_length=20, choices=transact_type_choices, default='OUT')
    transact_date = models.DateField()

    pallet = models.CharField(max_length=20)
    sf_code = models.CharField(max_length=20)

    product_type = models.CharField(max_length=10, null=True)
    product_name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)

    box_qty = models.FloatField(null=True, blank=True)  # CTN only
    pallet_qty = models.FloatField(null=True)

    bbd = models.DateField(null=True)
    pickup_by_choices = (
        ('NA', 'N/A'),
        ('CTN', 'CTN'),
        ('PACK', 'PACK')
    )
    pickup_by = models.CharField(max_length=20, choices=pickup_by_choices, default='CTN')
    memo = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = "CK Stock Transaction"
        verbose_name_plural = "CK Stock Transactions"
