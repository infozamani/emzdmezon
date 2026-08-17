from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from apps.orders.models import Order,OrderState
from apps.warehouses.models import Warehouse,WarehouseType
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Payment

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    # sandbox = 'www'
    sandbox = 'sandbox'

MERCHANT  =  "00000000-0000-0000-0000-000000000000"
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'http://127.0.0.1:8080/paymants/verify/'


#----------------------------------------------------------------------------------
class ZarinpalPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            user = request.user
            req_data = {
            "merchant_id": MERCHANT,
            "amount": order. get_order_total_price(),
            "Description": 'پرداخت از طریق درگاه زرین پال انجام شد',
            "CallbackURL": CallbackURL,
            "metadata":{'mobile':user.mobile_number, 'email':user.email},
        }
            req_header = {'content-type': 'application/json', 'accept': 'application/json' }
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json)['errors'] == 0:
                return redirect(ZP_API_STARTPAY.format(athority=authority))
            else:
                e_code = req.json(['errors']['code'])
                e_message = req.json(['errors']['message'])
                # e_code = req.json().get('errors', {}).get('code')
                # e_message = req.json().get('errors', {}).get('message')
                return HttpResponse(f"Error code:{e_code}, Error Message: {e_message}")
        except ObjectDoesNotExist:
            return redirect('payments:zarinpal_payment', order_id)
#----------------------------------------------------------------------------------
class ZarinpalPamentVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        t_stautus = request.GET.get('Status')
        t_authority = request.GET['authorrity']
        if request.GET.get('Status') == 'OK':
            order_id = request.session['payment_session']['order_id']    
            payment_id = request.session['payment_session']['payment_id']    
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.get(id=payment_id)
            
            req_header = {'content-type': 'application/json', 'accept': 'application/json' }
            req_data = {
            "merchant_id": MERCHANT,
            "amount": order. get_order_total_price(),
            "authorrity" :t_authority
            }
            
            req = request.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_stautus = req.json()['data']['code']
                
                if t_stautus == 100:
                    order.is_finaly = True
                    order.order_state = OrderState.objects.get(id=1)
                    order.save()
                    payment.is_finally = True
                    payment.status_code =t_stautus
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                #برای نشان دادن اضافه یا فروش کالاها پس از پرداخت مشتری 
                    for item in order.orders_details1.all():
                        Warehouse.objects.create(
                            warehouse_type = WarehouseType.objects.get(id=2),
                            user_registered = request.user,
                            product = item.product,
                            qty = item.qty,
                            price = item.price
                        )
                    
                    return HttpResponse('Transactive success.\nRefID:' + str(req.json()['data']['ref_id']))
                
                elif t_stautus == 101:
                    order.is_finaly = True
                    order.save()    
                    payment.is_finally = True
                    payment.status_code = t_stautus
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                                    #برای نشان دادن اضافه یا فروش کالاها پس از پرداخت مشتری 
                    for item in order.orders_details1.all():
                        Warehouse.objects.create(
                            warehouse_type = WarehouseType.objects.get(id=2),
                            user_registered = request.user,
                            product = item.product,
                            qty = item.qty,
                            price = item.price
                        )
                    return HttpResponse('Transactive submitted :' + str(req.json()['data']['message']))
                
                else:
                    payment.status_code = t_stautus 
                    payment.save()
                    return HttpResponse('Transactive failed.\nStatus:' + str(req.json()['data']['message']))
            else:
                e_code = req.json()['errors']['code']        
                e_message = req.json()['errors']['message']        
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse  ('Transactive failed or canceled by user' )