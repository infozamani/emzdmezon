# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Brand, ProductGroup, FeatureValue
from django.db.models import Q, Count, Min, Max
from django.views import View
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
from django.http import JsonResponse, HttpResponse
from apps.comment_scoring_favorites.models import Favorite
from apps.accounts.models import Customer
from django.contrib import messages


def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))


# ============================================================
# ارزانترین محصولات
# ============================================================
def get_cheapest_product(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:8]
    product_groups = get_root_group()
    context = {
        "products": products,
        "product_groups": product_groups
    }
    return render(request, "product_app/partials/cheapest_product.html", context)


# ============================================================
# جدیدترین محصولات
# ============================================================
def get_last_product(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:6]
    product_groups = get_root_group()
    context = {
        "products": products,
        "product_groups": product_groups
    }
    return render(request, "product_app/partials/last_product.html", context)


# ============================================================
# گروه محصولات محبوب
# ============================================================
def get_popular_product_groups(request, *args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True))\
                     .annotate(count=Count('products_of_groups'))\
                     .order_by('-count')[:6]
    context = {
        "product_groups": product_groups
    }
    return render(request, "product_app/partials/popular_product_groups.html", context)


# ============================================================
# جزئیات محصول (اصلاح شده)
# ============================================================
class productDetaileView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            # دریافت همه تصاویر گالری
            gallery_images = product.gallery_product.all()
            
            # دریافت محصولات مرتبط
            related_products = []
            for group in product.product_group.all():
                related_products.extend(
                    Product.objects.filter(
                        Q(is_active=True) & 
                        Q(product_group=group) & 
                        ~Q(id=product.id)
                    )[:3]
                )
            
            context = {
                'product': product,
                'gallery_images': gallery_images,
                'related_products': related_products,
            }
            return render(request, "product_app/product_details.html", context)
        return redirect('main:index')


# ============================================================
# محصولات مرتبط
# ============================================================
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(
            Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)
        ))
    return render(request, "product_app/partials/related_products.html", {'related_products': related_products})


# ============================================================
# لیست همه گروه‌های محصولات
# ============================================================
class ProductGroupView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True))\
                     .annotate(count=Count('products_of_groups'))\
                     .order_by('-count')
        return render(request, "product_app/product_groups.html", {'product_groups': product_groups})


# ============================================================
# گروه‌های محصولات برای فیلتر
# ============================================================
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                        .filter(Q(is_active=True) & ~Q(count=0))\
                                        .order_by('-count')
    return render(request, 'product_app/partials/product_groups.html', {'product_groups': product_groups})


# ============================================================
# برندها برای فیلتر
# ============================================================
def get_brands(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id = product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id)\
                            .annotate(count=Count('brands'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request, 'product_app/partials/brands_filter.html', {'brands': brands})


# ============================================================
# ویژگی‌ها برای فیلتر
# ============================================================
def get_feature_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list = product_group.Features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_value.all()
    return render(request, 'product_app/partials/features_filter.html', {'feature_dict': feature_dict})


# ============================================================
# لیست محصولات یک گروه با فیلتر
# ============================================================
class ProductsBygroupView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)
        
        # ===== اعمال order_by در ابتدای کوئری =====
        products = Product.objects.filter(
            Q(is_active=True) & Q(product_group=current_group)
        ).order_by('-id')  
        
        res_aggre = products.aggregate(min=Min('price'), max=Max('price'))
        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs
        
        brands_filter = request.GET.getlist('brand')
        if brands_filter:
            products = products.filter(brand__id__in=brands_filter)
        
        features_filter = request.GET.getlist('feature')
        if features_filter:
            products = products.filter(product_features__filter_value__id__in=features_filter).distinct()
        
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = "0"
        elif sort_type == "1":
            products = products.order_by('price')
        elif sort_type == "2":
            products = products.order_by('-price')
        
        group_slug = slug
        product_per_page = 10
        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
        
        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
        
        new_products = Product.objects.filter(is_active=True).order_by('-id')[:5]
        
        context = {
            'products': products,
            'current_group': current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_count_product': show_count_product,
            'filter': filter,
            'sort_type': sort_type,
            'new_products': new_products,
        }
        return render(request, "product_app/products.html", context)


# ============================================================
# دراپ‌داون ادمین
# ============================================================
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)


# ============================================================
# لیست مقایسه
# ============================================================

class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        context = {
            'compare_list': compare_list,
        }
        return render(request, 'product_app/compare_list.html', context)


def compare_table(request):
    """نمایش جدول مقایسه محصولات"""
    compareList = CompareProduct(request)
    
    products = []
    for productId in compareList.compare_product:
        try:
            product = Product.objects.get(id=productId, is_active=True)
            products.append(product)
        except Product.DoesNotExist:
            compareList.delete_form_compare_product(productId)
    
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
    
    context = {
        'products': products,
        'features': features,
        'compare_count': len(products),
    }
    return render(request, 'product_app/partials/compare_table.html', context)


def status_of_compare_list(request):
    """دریافت تعداد محصولات در لیست مقایسه"""
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)


# apps/products/views.py

def add_to_compare_list(request):
    """افزودن محصول به لیست مقایسه (AJAX)"""
    product_id = request.GET.get('productId')
    
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'شناسه محصول ارسال نشده است'})
    
    compareList = CompareProduct(request)
    result = compareList.add_to_compare_product(product_id)
    
    # ✅ دریافت ویژگی‌ها برای نمایش در جدول
    products = Product.objects.filter(id__in=compareList.compare_product)
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
    
    if result:
        return JsonResponse({
            'status': 'success',
            'message': 'محصول به لیست مقایسه اضافه شد',
            'compare_count': compareList.count,
            'features_count': len(features)
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'این محصول قبلاً در لیست مقایسه وجود دارد یا تعداد از ۴ بیشتر شده است',
            'compare_count': compareList.count
        })


def delete_from_compare_list(request):
    """حذف محصول از لیست مقایسه"""
    product_id = request.GET.get('productId')
    
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'شناسه محصول ارسال نشده است'})
    
    compareList = CompareProduct(request)
    compareList.delete_form_compare_product(product_id)
    
    return JsonResponse({
        'status': 'success',
        'message': 'محصول از لیست مقایسه حذف شد',
        'compare_count': compareList.count
    })


def clear_compare_list(request):
    """خالی کردن لیست مقایسه"""
    compareList = CompareProduct(request)
    compareList.clear_compare_product()
    
    return JsonResponse({
        'status': 'success',
        'message': 'لیست مقایسه خالی شد',
        'compare_count': 0
    })


# ============================================================
# علاقه‌مندی‌ها
# ============================================================

def status_of_favorite_list(request):
    """دریافت تعداد علاقه‌مندی‌های کاربر"""
    count = 0
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            count = Favorite.objects.filter(favorite_user=customer).count()
        except Customer.DoesNotExist:
            count = 0
        except Exception as e:
            count = 0
    return HttpResponse(count)


def toggle_favorite(request):
    """افزودن/حذف علاقه‌مندی (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'لطفاً ابتدا وارد شوید'})
    
    product_id = request.GET.get('productId')
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'شناسه محصول ارسال نشده است'})
    
    try:
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(user=request.user)
        
        favorite, created = Favorite.objects.get_or_create(
            favorite_user=customer,
            product=product
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
            message = 'محصول از علاقه‌مندی‌ها حذف شد'
        else:
            is_favorite = True
            message = 'محصول به علاقه‌مندی‌ها اضافه شد'
        
        count = Favorite.objects.filter(favorite_user=customer).count()
        
        return JsonResponse({
            'status': 'success',
            'message': message,
            'is_favorite': is_favorite,
            'favorite_count': count
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Customer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'کاربر یافت نشد'})

# ============================================================
# امتیازدهی
# ============================================================
def add_score(request):
    """افزودن امتیاز به محصول (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'لطفاً ابتدا وارد شوید'})
    
    product_id = request.GET.get('productId')
    score = request.GET.get('score')
    
    if not product_id or not score:
        return JsonResponse({'status': 'error', 'message': 'اطلاعات ناقص است'})
    
    try:
        score = int(score)
        if score < 1 or score > 5:
            return JsonResponse({'status': 'error', 'message': 'امتیاز باید بین 1 تا 5 باشد'})
        
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(user=request.user)
        
        # ثبت یا بروزرسانی امتیاز
        from apps.comment_scoring_favorites.models import Score
        score_obj, created = Score.objects.get_or_create(
            product=product,
            user=customer,
            defaults={'score': score}
        )
        if not created:
            score_obj.score = score
            score_obj.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'امتیاز شما با موفقیت ثبت شد',
            'score': score
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Customer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'کاربر یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})