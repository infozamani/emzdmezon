from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from CustomPermissions import CustomPermissionsForProducts
from .seializers import Productserializer
from apps.products.models import Product
#----------------------------------------------------------------
##creating a Api for models products
class AllproductsApi(APIView):
    Permission_classes = [CustomPermissionsForProducts]
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('published_date')
        self.check_object_permissions(request,products)
        ser_data = Productserializer(instance=products, many=True)
        return Response(data=ser_data.data)