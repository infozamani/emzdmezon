from django.contrib import admin
from .models import Warehouse,WarehouseType

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ('warehouse_type_title',)
@admin.register(Warehouse)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ('warehouse_type','user_registered','product','qty','price','register_date')
