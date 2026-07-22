from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Brand, ProductGroup,FeatureValue
from django.db.models import Q,Count,Min,Max
from django.views import View
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
from django.http import JsonResponse  
from django.http import HttpResponse
from apps.comment_scoring_favorites.models import Favorite

def get_root_group():
    return ProductGroup.objects.filter(Q(is_active = True)& Q(group_parent = None))

## ارزانترین محصولات
def get_cheapest_product(request,*args, **kwargs):
    products = Product.objects.filter(is_active = True).order_by('price')[:8]
    product_groups = get_root_group()
    context = {
        "products":products,
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/cheapest_product.html",context)
#--------------------------------------------------------------------
## جدیدترین محصولات(annotate)برای اضافه کردن فیلد یا ستون که برای شمارش وجمع و میانگین
def get_last_product(request,*args, **kwargs):
    products = Product.objects.filter(is_active = True).order_by('-published_date')[:6]
    product_groups = get_root_group()
    context = {
        "products":products,
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/last_product.html",context)
#--------------------------------------------------------------------
## گروه محصولات محبوب
def get_popular_product_groups(request,*args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('products_of_groups'))\
                     .order_by('-count')[:6]
    context = {
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/popular_product_groups.html",context)
#--------------------------------------------------------------------
## جزئیات محصول 
class productDetaileView(View):
    def get(self,request,slug):
        product = get_object_or_404(Product,slug = slug)
        if product.is_active:
            return render (request,"product_app/product_details.html",{'product':product})
#--------------------------------------------------------------------
## create related product 
def get_related_products(request,*args, **kwargs):
    current_prodouct = get_object_or_404(Product,slug=kwargs['slug'])
    related_product = []
    for group in current_prodouct.product_group.all():
        related_product.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group)& ~Q(id=current_prodouct.id)))
    return render (request,"product_app/partials/related_products.html" ,{'related_product':related_product})          
#--------------------------------------------------------------------
## create class list page  is all  products 
class ProductGroupView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('products_of_groups'))\
                     .order_by('-count')
        return render(request,"product_app/product_groups.html",{'product_groups':product_groups})
#------------------------------ filters --------------------------------------
## create class list group products for filter
def get_product_groups(request):
    product_groups =ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                        .filter(Q(is_active = True) & ~Q(count = 0))\
                                        .order_by('-count')
    
    return render(request,'product_app/partials/product_groups.html',{'product_groups':product_groups})
#--------------------------------------------------------------------
## create class list brands  products for filter 
def get_brands(request,*args, **kwargs):
    prodouct_group = get_object_or_404(ProductGroup,slug=kwargs['slug'])
    brand_list_id = prodouct_group.products_of_groups.filter(is_active = True).values('brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id)\
                            .annotate(count = Count('brands'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request,'product_app/partials/brands_filter.html',{'brands':brands})
#--------------------------------------------------------------------
## create class lists orther filters bar hasb feature products in the group
def get_feature_for_filter(request,*args, **kwargs):
    prodouct_group = get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list =prodouct_group.Features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_value.all()
    return render(request,'product_app/partials/features_filter.html',{'feature_dict ':feature_dict })
    
    #-----------------------------------------------------------------------------------------------
## create def list page  is one of  products 
class ProductsBygroupView(View):
    def get(self,request,*args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup,slug=slug)
        products = Product.objects.filter(Q(is_active = True) & Q(product_group = current_group))
        
        #--------------------------------------------
        ## price filter
        res_aggre = products.aggregate(min=Min('price'),max = Max('price'))
        filter = ProductFilter(request.GET,queryset = products)
        products = filter.qs
        
        #--------------------------------------------
        ## brand filter
        brands_filter = request.GET.getlist('brand')
        if brands_filter :
            products = products.filter(brand__id__in = brands_filter)
            
        #--------------------------------------------     
        ## features filter
        features_filter = request.GET.getlist('feature')
        if features_filter :
            products = products.filter(product_features__filter_value__id__in = features_filter).distinct()
             
        #--------------------------------------------  
        ## sort type
        sort_type = request.GET.get('sort_type')
        if not sort_type :
            sort_type = "0"
        elif sort_type == "1":
            products = products.order_by('price')
        elif sort_type == "2":
            products = products.order_by('-price')
            
        group_slug = slug
        product_per_page = 10                #تعداد کالاها در هر صفحه
        paginator = Paginator(products, product_per_page) 
        page_number = request.GET.get('page')       #بدست آوردن شماره صفحه جاری
        page_obj = paginator.get_page(page_number)  #صفحه بندی برای نمایش صفحه جاری
        product_count = products.count(); #تعداد کل مالاهای موجود در این گروه
        
        ##list numbers for make type open for number kala in page user
        show_count_product = []
        i = product_per_page
        while i < product_count :
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
        context = {
            'products': products,
            'current_group': current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_count_product':show_count_product,
            'filter': filter,
            'sort_type': sort_type,
        }

        return render(request,"product_app/products.html",context)

#----------------------------------------------------------------
## tow dropdown in admin panel
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False) 
#----------------------------------------------------------------
## صفحه اصلی مقایسه کالا ها:نمایش کالا های اضافه شده به لیست
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        context = {
            'compare_list': compare_list,
        }
        return render(request,'product_app/compare_list.html', context)
#----------------------------------------------------------------
## صفحه اصلی مقایسه کالا ها:نمایش کالا های اضافه شده به لیست
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        context = {
            'compare_list': compare_list,
        }
        return render(request,'product_app/compare_list.html', context)
#----------------------------------------------------------------
## نمایش جدول کالا های لیست مقایسه
def compare_table(request):
    compareList = CompareProduct(request)
    
    products = []
    for productId in compareList.compare_product:
        product = Product.objects.get(id=productId)
        products.append(product)
         
    features = []
    for product in products: 
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
        
        context ={
            'products' : products,
            'features' : features,
        }
        return render(request,'product_app/partials/compare_table.html',context)
#----------------------------------------------------------------
## Calculate the number of mod items in the comparison list محاسبه تعدا کالاهای موجود در لیست مقایسه
def status_of_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)

#----------------------------------------------------------------
##اضافه کردن کالا به لیست مقایسه=Add Items to Comparison List
def add_to_compare_list(request):
    productId = request.GET.get('productId')
    # ProductGroupId = request.GET.get('ProductGroupId')
    compareList = CompareProduct(request)
    compareList.add_to_compare_product(productId)
    # compareList.add_to_compare_product(ProductGroupId)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')

#----------------------------------------------------------------
## حذف کالا از لیست مقایسه =  Remove the item from the comparison list 
def delete_from_compare_list(request):
    productId = request.GET.get('productId')
    compareList = CompareProduct(request)
    compareList.delete_form_compare_product(productId)
    return redirect("products:compare_table")
#----------------------------------------------------------------
## Calculate the number of mod items in the comparison list محاسبه تعدا کالاهای موجود در لیست مقایسه
def status_of_favorite_list(request):
    favoritelist = Favorite(request)
    return HttpResponse(favoritelist.count)
