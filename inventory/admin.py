from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import (DropdownFilter)
# Register your models here.

@admin.register(Stock)
#class ViewAdmin(admin.ModelAdmin):
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['update_date', 'product_type', 'sf_code', 'origin', 'inward', 'product_name', 'new_balance', 'unit', 'bbd', 'location']
    search_fields = ['sf_code', 'product_name', 'update_date', 'location']
    filter_horizontal = ()
    list_filter = ['update_date', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('product_name', DropdownFilter), ('unit', DropdownFilter), ('location', DropdownFilter)]
    date_hierarchy = 'update_date'
    fieldsets = ()
    


@admin.register(CurrentStock)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['end_stock_day', 'product_type', 'sf_code',  'new_balance', 'unit', 'bbd']
    search_fields = ['sf_code']
    filter_horizontal = ()
    list_filter = [('product_type', DropdownFilter), ('sf_code', DropdownFilter)]
    date_hierarchy = 'end_stock_day'
    fieldsets = ()

@admin.register(Usage)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['update_date','product_type', 'sf_code','product_name', 'pickup_qty', 'unit', 'memo']
    search_fields = ['sf_code', 'update_date', 'memo', 'product_name']
    filter_horizontal = ()
    list_filter = ['update_date', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('unit', DropdownFilter)]
    date_hierarchy = 'update_date'
    fieldsets = ()

@admin.register(MonthlyUsage)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['usage_month', 'product_type', 'sf_code','product_name', 'monthly_usage', 'unit']
    search_fields = ['sf_code', 'usage_month']
    filter_horizontal = ()
    list_filter = ['usage_month', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('unit', DropdownFilter)]
    date_hierarchy = 'usage_month'
    fieldsets = ()

@admin.register(aDailyUsage)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['update_date','product_type', 'sf_code','origin', 'product_name', 'pickup_qty', 'unit', 'memo']
    search_fields = ['sf_code', 'update_date', 'memo', 'product_name']
    filter_horizontal = ()
    list_filter = ['update_date', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('unit', DropdownFilter)]
    date_hierarchy = 'update_date'
    fieldsets = ()
    
@admin.register(aDailyStock)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['update_date', 'product_type', 'sf_code', 'origin', 'inward', 'product_name', 'new_balance', 'unit', 'bbd', 'location']
    search_fields = ['sf_code', 'product_name', 'update_date', 'location']
    filter_horizontal = ()
    list_filter = ['update_date', ('product_type', DropdownFilter), ('sf_code', DropdownFilter), ('product_name', DropdownFilter), ('unit', DropdownFilter), ('location', DropdownFilter)]
    date_hierarchy = 'update_date'
    fieldsets = ()
  
@admin.register(StorageTransactLog)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['transact_date', 'transact_time', 'storage_loc', 'total_pallet_before_transaction', 'transact_type', 'pallet_qty', 'total_pallet_after_transaction']
    search_fields = ['transact_date', 'storage_loc', 'transact_type' ]
    filter_horizontal = ()
    list_filter = ['transact_date', ('storage_loc', DropdownFilter), ('transact_type', DropdownFilter)]
    date_hierarchy = 'transact_date'
    fieldsets = ()

@admin.register(StoragePalletQty)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ['storage_loc', 'total_pallet_qty']