from django.db import models

# Create your models here.
class MonthlyUsage(models.Model):
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    usage_month = models.DateField()
    monthly_usage = models.FloatField(null=True)
    unit = models.CharField(max_length=20, null=True)#, choices=unit_choices)

    class Meta:
        verbose_name = "Main Monthly Usage"
        verbose_name_plural = "Main Monthly Usages"

    def __str__(self):
        return '({0}) {1}'.format(self.usage_month, self.sf_code)


class Usage(models.Model):
    update_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    pickup_qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)#, choices=unit_choices)
    memo = models.CharField(max_length=300)

    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = "Main Usage"
        verbose_name_plural = "Main Usages"

    def __str__(self):
        return '({0}) {1} - {2} {3}'.format(self.update_date, self.sf_code, self.pickup_qty, self.unit)


class CurrentStock(models.Model):
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    end_stock_day = models.DateField()
    #product_name = models.CharField(max_length=300, null=True)
    new_balance = models.FloatField()
    unit = models.CharField(max_length=20)
    bbd = models.DateField(null=True)

    class Meta:
        verbose_name = "Main Aggregated Stock"
        verbose_name_plural = "Main Aggregated Stocks"


class Stock(models.Model):
    update_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    inward = models.DateField(null=True)
    product_name = models.CharField(max_length=300, null=True)
    new_balance = models.FloatField()
    
    unit = models.CharField(max_length=20)
    bbd = models.DateField(null=True)
    # Storage location
    location = models.CharField(max_length=20, null=True)
    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)
    
    #class Meta:
    #    abstract = True
    class Meta:
        verbose_name = "Main Stock"
        verbose_name_plural = "Main Stocks"

    def __str__(self):
        return '({0}) {1}'.format(self.update_date, self.sf_code)


class ProductList(models.Model):
    sf_code = models.CharField(max_length=20)
    product_type = models.CharField(max_length=10, null=True)
    product_name = models.CharField(max_length=300, null=True)


class NotUsedProductList(models.Model):
    sf_code = models.CharField(max_length=20)
    product_type = models.CharField(max_length=10, null=True)
    product_name = models.CharField(max_length=300, null=True)


class aDailyUsage(models.Model):
    update_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    pickup_qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)#, choices=unit_choices)
    memo = models.CharField(max_length=300)

    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = "Daily Usage"
        verbose_name_plural = "Daily Usages"

    def __str__(self):
        return '({0}) {1} - {2} {3}'.format(self.update_date, self.sf_code, self.pickup_qty, self.unit)

class aDailyStock(models.Model):
    update_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    inward = models.DateField(null=True)
    product_name = models.CharField(max_length=300, null=True)
    new_balance = models.FloatField()
    
    unit = models.CharField(max_length=20)
    bbd = models.DateField(null=True)
    # Storage location
    location = models.CharField(max_length=20, null=True)
    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)
    
    #class Meta:
    #    abstract = True
    class Meta:
        verbose_name = "Daily Stock"
        verbose_name_plural = "Daily Stocks"

    def __str__(self):
        return '({0}) {1}'.format(self.update_date, self.sf_code)



class StorageTransactLog(models.Model):
    transact_date = models.DateField()
    transact_time = models.TimeField()    
    storage_loc_choices = (
        ('LW', 'Lucky Winner'),
        ('OS', 'OSP'),
        ('HS', 'Haison'),
        ('HE', 'Hellman'),
        ('HX', 'HerbX'),
    )
    storage_loc = models.CharField(max_length=10, choices=storage_loc_choices, default='LW')     
    transaction_type_choices = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),        
    )
    transact_type = models.CharField(max_length=20, choices=transaction_type_choices, default='OUT')
    total_pallet_before_transaction = models.FloatField(null=True)
    #total_pallet_before_transaction = models.ForeignKey(StoragePalletQty, on_delete=models.CASCADE)
        
    pallet_qty = models.FloatField(null=True)
    total_pallet_after_transaction = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Storage Transaction Log"
        verbose_name_plural = "Storage Transaction Logs"

    def save(self, *args, **kwargs):
        if self.transact_type == 'IN':
            self.total_pallet_after_transaction = self.total_pallet_before_transaction + self.pallet_qty
        else:
            self.total_pallet_after_transaction = self.total_pallet_before_transaction - self.pallet_qty
        super(StorageTransactLog, self).save(*args, **kwargs)