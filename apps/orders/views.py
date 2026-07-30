from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from .models import Order,OrderDetails
from .form import OrderForm
from .models import PaymentType
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupons
from django.db.models import Q
from datetime import datetime
from django.contrib import messages

class ShopCartView(View):
    def get(self,request, *args, **kwargs) :
        shop_cart = ShopCart(request)
        return render (request, 'orders_app/shop_cart.html', {'shop_cart':shop_cart})
    
# ---------------------------------------------------------------------
## برای آپدیت از سبد کالا
def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart = ShopCart(request)
    shop_cart.update(product_id_list, qty_list)
    return redirect("orders:show_shop_cart")
# ---------------------------------------------------------------------
# تابع برای نشان دادن رکوردها از سبد مالا
def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price = shop_cart.calc_total_price()
    delivery = 25000
    if total_price > 500000:
        delivery = 0
        
    tax = 0.09 * total_price
    final_total_price = total_price +delivery + tax
    context ={
        'shop_cart':shop_cart,
        'shop_cart_count':shop_cart.count,
        'total_price':total_price,
        'delivery':delivery,
        'tax':tax,
        'final_total_price' :final_total_price
        }
    return render (request,"orders_app/partials/show_shop_cart.html",context)

# ---------------------------------------------------------------------
# تابع برای اضافه کردن به سبد مالا
def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product,id = product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return  HttpResponse(shop_cart.count)
# ---------------------------------------------------------------------
## برای حذف از سبد کالا
def delete_form_shop_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product,id = product_id)
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")
   

# ---------------------------------------------------------------------
## برای نمایش تعداد  از سبد کالا
def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)
# ---------------------------------------------------------------------
## برای مجبور کردن مشتری برای ورود
class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request):
        try:
            customer = Customer.objects.get(user = request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create( user = request.user)
             
        order = Order.objects.create(customer = customer, payment_type = get_object_or_404(PaymentType, id = 1))
        shop_cart = ShopCart(request)
        for item in shop_cart:
            OrderDetails.objects.create(
            order = order,
            product = item['product'],
            price = item['price'],
            qty = item['qty'],
            
        )
        
        return redirect('orders:checkout_order', order.id)
# ---------------------------------------------------------------------
## برای مجبور کردن مشتری برای ورودادامه پرداخت 
class CheckoutOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        shop_cart = ShopCart(request)
        order = get_object_or_404(Order,id=order_id)
        total_price = shop_cart.calc_total_price()
        delivery = 25000
        if total_price > 500000:
            delivery = 0
        tax = 0.09 * total_price
        final_total_price = total_price +delivery + tax
        if order.discount > 0:
            final_total_price = final_total_price - (final_total_price * order.discount/100)
            
        data = {
            'name' :user.name,
            'family':user.family,
            'email': user.email,
            'phone_number': customer.phone_number,
            'description' :order.description,
            'payment_type' :order.payment_type,
        }
        form = OrderForm(data)
        form_coupon = CouponForm()
        context = {
            'shop_cart': shop_cart,
            'total_price': total_price,
            'delivery': delivery,
            'tax': tax,
            'final_total_price': final_total_price,
            'form' : form, 
            'form_coupon':form_coupon, 
            'order':order ,
               
        }
        return render(request,'orders_app/checkout.html',context)
    
    #-------------------------------------------------------
    def post(self, request, order_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                order = Order.objects.get(id = order_id)
                order.description = cd['description']
                order.payment_type = PaymentType.objects.get(id = cd['payment_type'])
                order.save()
                
                user = request.user
                user.name = cd['name']              
                user.family = cd['family']              
                user.email = cd['email']              
                user.save()  
                
                customer = Customer.objects.get(user = user)
                customer.phone_number = cd['phone_number']
                customer.address = cd['address']
                customer.save()
                # messages.success(request,'اطلاعات با موفقیت ثبت شد')
                return redirect('payments:zarinpal_payment', order_id)
            except ObjectDoesNotExist:
               messages.error(request,'فاکتور با این مشخصات یافت نشد','danger')
        return redirect('orders:checkout_order', order_id)   
# ---------------------------------------------------------------------
##create order application coupon
class ApplayCoupon(View):
    def post(self,request,*args, **kwargs):
        order_id = kwargs['order_id']
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            cd = coupon_form.cleaned_data
            coupon_code = cd['coupon_code']
            coupon = Coupons.objects.filter(
                        Q(coupon_code = coupon_code)&
                        Q(is_active = True)&
                        Q(start_date__lte = datetime.now())&
                        Q(end_date__gte = datetime.now())  
            )
            discount = 0
            try:
                order = Order.objects.get(id=order_id)
                if coupon :
                    discount = coupon[0].discount
                    order.discount = discount
                    order.save()
                    messages.success(request,'اعمال کوپن با موفقیت انجام شد')
                    return redirect('orders:checkout_order', order_id)
                else:
                    order.discount = discount
                    order.save()
                    messages.error(request,'کد وارد شده معتبرنمی باشد','danger')
            except ObjectDoesNotExist:
                    messages.error(request,'سفارش موجود نیست')
            return redirect('orders:checkout_order', order_id)


 
def status_of_shop_cart(request):
    """دریافت تعداد سبد خرید"""
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)

def status_of_favorites(request):
    """دریافت تعداد علاقه‌مندی‌ها"""
    count = 0
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            from apps.comment_scoring_favorites.models import Favorite
            count = Favorite.objects.filter(customer=customer).count()
        except:
            count = 0
    return HttpResponse(count)

def status_of_compare(request):
    """دریافت تعداد مقایسه"""
    count = 0
    if request.session.get('compare_list'):
        count = len(request.session.get('compare_list'))
    return HttpResponse(count)