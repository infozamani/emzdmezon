from django.db import models
from apps.products.models import Product
from apps.accounts.models import Customer
#----------------------------------------------------------------
class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50, verbose_name='نوع انبار')

    
    def __str__(self) -> str:
        return f"{self.warehouse_type_title}"
    
    
    class Meta:
        verbose_name = 'نوع انیار'
        verbose_name_plural = 'انواع روش انبار'
#----------------------------------------------------------------
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType, verbose_name="انبار", on_delete=models.CASCADE, related_name='warehouses')
    user_registered = models.ForeignKey(Customer, verbose_name="کاربر", on_delete=models.CASCADE,related_name='warehouses_Customuser')
    product = models.ForeignKey(Product, verbose_name="کالا", on_delete=models.CASCADE,related_name='warehouses_prouduct' )
    qty = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت واحد',null=True, blank=True)
    register_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add = True)
    
    
    def __str__(self) -> str:
        return f"{self.warehouse_type} - {self.product}"
    
    
    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'