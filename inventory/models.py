from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .sf_notify import * 


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

    location = models.CharField(max_length=20, null=True)
    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)

    cust_name = models.CharField(max_length=150, null=True)

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

    cust_name = models.CharField(max_length=150, null=True)

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
        ('LW(D)', 'Lucky Winner (Dry)'),
        ('OS', 'OSP'),
        ('HS', 'Haison'),
        ('HE', 'Hellman'),
        ('HX', 'HubX'),
    )
    storage_loc = models.CharField(max_length=10, choices=storage_loc_choices, default='LW')
    transaction_type_choices = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),
    )
    transact_type = models.CharField(max_length=20, choices=transaction_type_choices, default='OUT')
    total_pallet_before_transaction = models.FloatField(null=True)
    #total_pallet_before_transaction = models.ForeignKey(StoragePalletQty, on_delete=models.CASCADE)
    box_qty = models.FloatField(null=True, blank=True)

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


class NoodleUsage(models.Model):
    update_date = models.DateField()
    customer = models.CharField(max_length=30, null=True)
    sf_code = models.CharField(max_length=20, null=True)
    simple_name = models.CharField(max_length=20, null=True)
    product_name = models.CharField(max_length=300, null=True)
    qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Noodle Product Usage"
        verbose_name_plural = "Noodle Product Usages"


class NoStockItems(models.Model):        
    sf_code = models.CharField(max_length=20, null=True)    
    product_name = models.CharField(max_length=300, null=True)
    product_spec = models.CharField(max_length=300, null=True)

    container_name_choices = (
        ('COF', 'COF'),
        ('EEL', 'EEL'),
        ('FO', 'FO'),
        ('GN', 'GN'),
        ('Gyoren', 'Gyoren'),
        ('ITABASHI', 'ITABASHI'),
        ('LUF', 'LUF'),
        ('NW', 'NW'),
        ('OIL', 'OIL'),
        ('QP', 'QP'),
        ('STI', 'STI'),
        ('TEP', 'TEP'),
        ('TWIN', 'TWIN'),
        ('VFK', 'VFK'),
        ('YamasaFRZ', 'YamasaFRZ'),
        ('YM', 'YM'),
        
    )
    container_name = models.CharField(max_length=50, choices=container_name_choices, null=True, blank=True)    
    container_eta = models.DateField(null=True, blank=True)
    
    container_status_choices = (
        ('normal', 'Normal'),
        ('D1', 'Delay 1'),
        ('D2', 'Delay 2'),
        ('D3', 'Delay 3'),
        ('D4', 'Delay 4'),
        ('D5', 'Delay 5'),
        ('D6', 'Delay 6'),
    )
    container_status = models.CharField(max_length=30, choices=container_status_choices, null=True, blank=True)

    customer = models.CharField(max_length=100, null=True, blank=True)
    stock_status_choices = (
        ('closed', 'Closed'),
        ('nostock', 'No Stock'),
        ('controlling', 'Controlling'),        
    )
    stock_status = models.CharField(max_length=30, choices=stock_status_choices, null=True, blank=True)
    remark = models.TextField(blank=True, null=True)
    

    class Meta:
        verbose_name = "No Stock Item"
        verbose_name_plural = "No Stock Items"


@receiver(post_save, sender=NoStockItems)
def notify_staff(sender, instance, **kwargs):        
    send_message(instance.sf_code, instance.container_name)
    

