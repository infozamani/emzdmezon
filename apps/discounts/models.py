from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.products.models import Product
#------------------------------------------------------------------------------
## create copon discounts
class Coupons(models.Model):
    coupon_code = models.CharField(verbose_name='کد تخفیف', max_length=10,unique=True)
    start_date = models.DateTimeField(verbose_name='تاریخ شروع',auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(verbose_name='تاریخ خاتمه',auto_now=False, auto_now_add=False)
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators= [MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name='وضعیت')
    
    
    class Meta:
        verbose_name = 'کوپن تخفیف '
        verbose_name_plural = 'کوپن های تخفیف'
        
    def __str__(self) -> str:
        return self.coupon_code
#------------------------------------------------------------------------------
## create discount basket
class DiscountBasket(models.Model):
    discount_title = models.CharField(verbose_name='عنوان تخفیف ', max_length=100)
    start_date = models.DateTimeField(verbose_name='تاریخ شروع',auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(verbose_name='تاریخ خاتمه',auto_now=False, auto_now_add=False)
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators= [MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name='وضعیت')
    
    
    class Meta:
        verbose_name = 'سبد تخفیف '
        verbose_name_plural = 'سبدهای  تخفیف'
        
    def __str__(self) -> str:
        return self.discount_title
#------------------------------------------------------------------------------
## create Discount Basket Details
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, verbose_name=("سبد تخفیف"), on_delete=models.CASCADE,related_name='discount_basket_detalis1')
    product = models.ForeignKey(Product, verbose_name=("کالا  "), on_delete=models.CASCADE,related_name='discount_baskets_detalis2')
    
    class Meta:
        verbose_name = 'جزِئیات سبد تخفیف'
#------------------------------------------------------------------------------