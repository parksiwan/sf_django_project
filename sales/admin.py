from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import *
from import_export.admin import ImportExportModelAdmin
#from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg
from django_admin_listfilter_dropdown.filters import (DropdownFilter)
# Register your models here.

'''
class MyChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(MyChangeList, self).get_results(*args, **kwargs)
        q1 = self.result_list.aggregate(sales_qty=Sum('sales_qty'))
        q2 = self.result_list.aggregate(pp=Sum('product_price'))
        self.sales_count = q1['sales_qty']
        self.sales_amount = q2['pp']
'''

@admin.register(Sales)
class ViewAdmin(ImportExportModelAdmin):
    list_display =['customer', 'sales_date', 'product_code', 'product_name', 'sales_qty', 'product_cost', 'product_price', 'sales_amt', 'cost_amt']
    list_totals = [('pickup_qty', Sum)]
    search_fields = ['customer', 'sales_date', 'product_code', 'product_name', 'sales_qty', 'product_cost', 'product_price']
    filter_horizontal = ()
    list_filter = [('customer', DropdownFilter), 'sales_date', ('product_code', DropdownFilter), ('product_name', DropdownFilter)]
    date_hierarchy = 'sales_date'
    fieldsets = ()

    #change_list_template = 'admin/sales/sales/change_list.html'

    class Meta:
        model = Sales
    '''
    def get_changelist(self, request):
        return MyChangeList
    '''
    def sales_amt(self, obj):
        return "{:.2f}".format(obj.sales_qty * obj.product_price)

    def cost_amt(self, obj):
        return "{:.2f}".format(obj.sales_qty * obj.product_cost)
