from django.urls import path
from .views import ZarinpalPaymentView,ZarinpalPamentVerifyView

app_name = 'payments'
urlpatterns = [
    path('zarinpal_payment/',ZarinpalPaymentView.as_view(), name='zarinpal_payment' ),
    path('verify/',ZarinpalPamentVerifyView.as_view(), name='zarinpal_payment_verify' ),
   
]