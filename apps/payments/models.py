from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payment_order', on_delete=models.CASCADE, verbose_name='سفارش')
    customer = models.ForeignKey(Order, related_name='payment_customer', on_delete=models.CASCADE, verbose_name='مشتری')
    register_date = models.DateTimeField(verbose_name=("تاریخ درج"), default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش پرداخت    ')
    amount = models.IntegerField(verbose_name='مبلغ پرداخت')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات پرداخت')
    is_finally = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    
    status_code = models.IntegerField(verbose_name='کد وضعیت پرداخت',null=True, blank=True)
    ref_id = models.CharField(max_length=50, verbose_name='شماره پیگیر پرداخت', null=True, blank=True)
    
    def __str__(self):
        return f"{self.order}\t{self.customer}\t{self.ref_id}\t"
    
    class Meta:
        verbose_name = ("پرداخت ")
        verbose_name_plural =('پرداخت ها')