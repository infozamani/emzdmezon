from django.shortcuts import render, get_object_or_404, redirect 
from django.views import View
from .forms import CommentForm
from apps.comment_scoring_favorites.models import Comment
from apps.products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from apps.comment_scoring_favorites.models import Scoring, Favorite
from django.db.models import Q
from apps.orders.shop_cart import ShopCart
#----------------------------------------------------------------
## create a commentView with a form
class CommantView(View):
    def get(self,request, *args, **kwargs):
        productId = request.GET.get('productId')
        commentId = request.GET.get('commentId')
        slug = kwargs['slug']
        initial_dict = {
            "product_id": productId,
            "comment_id": commentId,
        }
        form = CommentForm(initial = initial_dict)
        return render(request, 'csf_app/partials/create_comment.html', {'form' :form, 'slug': slug})
   
    def post (self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = None
            if (cd['comment_id']):
                parentId = cd['comment_id'] 
                parent = Comment.objects.get(id=parentId)   
            Comment.objects.create(
                                product = product,
                                commenting_user = request.user,
                                comment_text = cd['comment_text'],
                                comment_parent = parent,
                                
                                )  
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details',product.slug)
        messages.error(request, 'خطا در ارسال نظر','danger')
        return redirect('products:product_details',product.slug)
#----------------------------------------------------------------
#--------------------------------------
## create add score function
def add_score(request):
    productId = request.GET.get('productId')
    score = request.GET.get('score')
    
    product = Product.objects.get(id=productId)
    
    Scoring.objects.create(
        product=product,
        scoring_user = request.user,
        score = score,
    ) 
    return HttpResponse ('امتیاز شما با موفقیت ثبت شد')
#----------------------------------------------------------------
##create a add favorite
def add_to_favorite(request):
    productId = request.GET.get('productId')
    product = Product.objects.get(id=productId)
    flag = Favorite.objects.filter(
                                    Q(favorite_user_id=request.user.id) & 
                                    Q(product_id=productId)).exists()
    if (not flag):
        Favorite.objects.create(
            product=product,
            favorite_user = request.user,
            )
        return HttpResponse('این کالا به لیست علایق شما اضافه شد')
    return  HttpResponse('این کالا قبلا در لیست علایق شما قرار گرفته')
          
#----------------------------------------------------------------
class  UserFavoriteView(View):
    def get(self, request, *args, **kwargs):
        user_favorite = Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request, 'csf_app/user_favorite.html', {'user_favorite': user_favorite}) 
# ---------------------------------------------------------------------
# تابع برای اضافه کردن به سبد علایق
def add_to_product_fvorite(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product,id = product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return  HttpResponse(shop_cart.count)                          
                                  
# ================================================================
# حذف از علاقه‌مندی‌ها (تابع جدید)
# ================================================================
def remove_from_favorite(request):
    productId = request.GET.get('productId')
    
    if not productId:
        return HttpResponse('error: productId required', status=400)
    
    if not request.user.is_authenticated:
        return HttpResponse('error: please login first', status=401)
    
    try:
        favorite = Favorite.objects.filter(
            Q(favorite_user_id=request.user.id) & 
            Q(product_id=productId)
        )
        if favorite.exists():
            favorite.delete()
            return HttpResponse('success: removed from favorites')
        else:
            return HttpResponse('error: not found in favorites', status=404)
    except Exception as e:
        return HttpResponse(f'error: {str(e)}', status=500)                                
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  