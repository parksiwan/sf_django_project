from django.db import models

# Create your models here.
class MonthlyUsage(models.Model):
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    usage_month = models.DateField()
    monthly_usage = models.FloatField(null=True)
    unit = models.CharField(max_length=20, null=True)#, choices=unit_choices)

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


class DailyUsage(models.Model):
    update_date = models.DateField()
    product_type = models.CharField(max_length=10, null=True)
    sf_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=300, null=True)
    pickup_qty = models.FloatField(null=True)
    unit = models.CharField(max_length=20)#, choices=unit_choices)
    memo = models.CharField(max_length=300)

    origin = models.CharField(max_length=10, null=True)
    product_name_jp = models.CharField(max_length=300, null=True)

    def __str__(self):
        return '({0}) {1} - {2} {3}'.format(self.update_date, self.sf_code, self.pickup_qty, self.unit)

class DailyStock(models.Model):
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
    def __str__(self):
        return '({0}) {1}'.format(self.update_date, self.sf_code)