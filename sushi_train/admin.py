from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.db.models import Sum, Avg
from django_admin_listfilter_dropdown.filters import (DropdownFilter)
# Register your models here.

@admin.register(PackingList)
class ViewAdmin(ImportExportModelAdmin):
    list_display =['customer', 'dispatch_date', 'sf_code', 'product_name', 'qty', 'unit']    
    search_fields = ['customer', 'dispatch_date', 'sf_code', 'product_name', 'qty', 'unit']
    filter_horizontal = ()
    list_filter = [('customer', DropdownFilter), 'dispatch_date', ('sf_code', DropdownFilter), ('product_name', DropdownFilter)]
    date_hierarchy = 'dispatch_date'
    fieldsets = ()

    class Meta:
        model = PackingList
   

