from django.urls import path
from .views import *

app_name = 'test_api'
urlpatterns = [
    path('products/',AllproductsApi.as_view(),name='products'),
]
