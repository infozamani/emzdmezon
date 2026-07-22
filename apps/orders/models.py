from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
# ----------------------------------------------------------------------------------------------
## class for pay manegment type
class PaymentType(models.Model):
    payment_title = models.CharField( max_length=50, verbose_name='نوع پرداخت')
    
    
    def __str__(self):
        return f"{self.payment_title}"
    
    class Meta:
        verbose_name = 'نوع پرداخت  '
        verbose_name_plural= 'انواع روش پرداخت ها' 
#----------------------------------------------------------------
class OrderState(models.Model):
    order_state_title = models.CharField(max_length=50,verbose_name='عنوان سفارش وضعیت کالا')
    
    def __str__(self) :
        return f"{self.order_state_title }"
    class Meta:
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'وضعیتهای  سفارش'
# ---------------------------------------------------------------
class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='مشتری', on_delete=models.CASCADE, related_name='orders')  
    update_date = models.DateField(verbose_name='تاریخ ویرایش سفارش', auto_now=True)
    register_date = models.DateField(verbose_name='تاریخ  درج سفارش', default=timezone.now)
    is_finaly = models.BooleanField(verbose_name='نهایی شده', default=False)
    order_code = models.UUIDField(verbose_name='کد برای سفارش', unique=True, default=uuid.uuid4, editable=False)
    discount = models.IntegerField(verbose_name='تخفیف روی فاکتور', default=0, null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    payment_type = models.ForeignKey(PaymentType,default=1, blank=True, null=True,related_name='payment_types', verbose_name="روش پرداخت", on_delete=models.CASCADE)
    order_state = models.ForeignKey(OrderState, verbose_name="وضعیت سفارش",  on_delete=models.CASCADE, related_name='order_states',null=True, blank=True) 
     
    def  get_order_total_price(self):
        sum = 0
        for item in self.orders_details1.all():
            sum += item.price * item.qty 
        delivery = 25000
        if sum > 500000:
            delivery = 0
        tax = sum * 0.09
        return int((sum + delivery + tax)*10)
        
     
    def __str__(self):
        return f"{self.customer}\t{self.id}\t{self.is_finaly}"
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات '
#----------------------------------------------------------------------------------------------
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, verbose_name='مشتری', on_delete=models.CASCADE, related_name='orders_details1')
    product = models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE, related_name='orders_details2')
    qty = models.PositiveIntegerField(verbose_name='تعداد',default=1)
    price = models.IntegerField(verbose_name='قیمت کالا در فاکتور')
    
    def __str__ (self):
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}"
      