from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import (DropdownFilter)
# Register your models here.

@admin.register(Stock)
#class ViewAdmin(admin.ModelAdmin):
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['stock_base_date', 'product_type', 'sf_code', 'plenus_code', 'product_name', 'description', 'qty', 'unit', 'bbd']
    search_fields = ['sf_code', 'product_name', 'stock_base_date']
    filter_horizontal = ()
    list_filter = ['stock_base_date', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('product_name', DropdownFilter)]
    date_hierarchy = 'stock_base_date'
    fieldsets = ()


@admin.register(MonthlyUsage)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['usage_month', 'product_type', 'customer', 'sf_code', 'product_name', 'qty', 'unit']
    search_fields = ['sf_code', 'usage_month', 'product_name']
    filter_horizontal = ()
    list_filter = ['usage_month', ('product_type', DropdownFilter), ('customer', DropdownFilter), ('sf_code', DropdownFilter), ('product_name', DropdownFilter)]
    date_hierarchy = 'usage_month'
    fieldsets = ()

    
@admin.register(CKStock)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['transact_type', 'transact_date', 'pallet', 'sf_code', 'product_name', 'box_qty', 'pickup_by', 'bbd']
    search_fields = ['sf_code', 'pallet', 'product_name']
    filter_horizontal = ()
    list_filter = [('pallet', DropdownFilter), ('sf_code', DropdownFilter), ('product_name', DropdownFilter)]
    date_hierarchy = 'transact_date'
    fieldsets = ()


