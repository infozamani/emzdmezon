from django.shortcuts import render
from django.views import View
from apps.products.models import Product
from django.db.models import Q
#----------------------------------------------------------------
## Creating search results class
class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(description__icontains=query)  #برای هر فیلد مربوط به آپ پروداکت می توانید ادامه دهید
        )
        # blog = Blog.objects.filter(
        #     Q(product_name__icontains=query) | 
        #     Q(description__icontains=query) | #برای هر فیلد مربوط به آپ مقالات می توانید ادامه دهید
        # )
        context = {
            'products' : products,
        }
        return render(request,'search_apps/search_results.html',context)
    
