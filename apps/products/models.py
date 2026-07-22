from django.db import models
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField 
# from ckeditor.fields import RichTextField 
from django.urls import reverse
from datetime  import datetime
from django.db.models import Sum,Avg
from middlewares.middlewares import RequestMiddleware
from django.db.models.signals import post_delete
from django.dispatch import receiver
 
#------------------------------------------------------------------------
## Creating a Brand class   
class Brand (models.Model):
    brand_name = models.CharField( max_length=100, verbose_name='نام برند')
    file_upload = FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر برند کالا')#برای اینکه فایل عمومی برای همه فیلد های مدل های مختلف داشته باشیم تابعی در پوشه مشترک می سازم 
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.brand_name
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = ' برند ها'

#------------------------------------------------------------------------
## creating a productgroups class
class ProductGroup (models.Model):
    group_title = models.CharField(max_length=500, verbose_name='عناوین کالا')
    file_upload = FileUpload('images', 'ProductGroup')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر گروه کالا')#برای اینکه فایل عمومی برای همه فیلد های مدل های مختلف داشته باشیم تابعی در پوشه مشترک می سازم 
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True,blank=True, verbose_name='وضعیت فعال /غیر فعال')
    group_parent = models.ForeignKey("ProductGroup", verbose_name="والد گروه کالا", on_delete=models.CASCADE, blank=True, null=True, related_name = 'groups') 
    register_date = models.DateTimeField(verbose_name=("تاریخ درج"), auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='آخرین بروز رسانی کالا')
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.group_title
    class Meta:
        verbose_name = 'گروه کالا'
        verbose_name_plural = ' گروه های کالا '
#------------------------------------------------------------------------
## create class Feature(ویژگیها)
class Feature (models.Model):
    feature_name = models.CharField(verbose_name=("نام ویژگی"), max_length=100)
    product_group = models.ManyToManyField(ProductGroup, verbose_name=("گروه کالا"), related_name = 'Features_of_groups')
 
    class Meta:
        verbose_name = ("ویژگی")
        verbose_name_plural =("ویژگی ها")  

    def __str__(self):
        return self.feature_name
#---------------------------------------------------------------------------------------------
## create class product
class Product(models.Model) :
    product_name = models.CharField(verbose_name = ("نام کالا"), max_length=500)
    # description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    summery_description = models.TextField(default="",blank=True, null=True, verbose_name=' توضیحات کوتاه')
    description = RichTextUploadingField(config_name = 'special',blank= None)
    file_upload = FileUpload('images', 'Product')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر  کالا')#برای اینکه فایل عمومی برای همه فیلد های مدل های مختلف داشته باشیم تابعی در پوشه مشترک می سازم 
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت کالا')
    is_active = models.BooleanField(default=True,blank=True, verbose_name='وضعیت فعال /غیر فعال')
    register_date = models.DateTimeField(verbose_name=("تاریخ درج"), auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='آخرین بروز رسانی کالا')
    product_group = models.ManyToManyField(ProductGroup, verbose_name=("گروه کالا"), related_name = 'products_of_groups')
    brand = models.ForeignKey(Brand, verbose_name=("برند کالا"), on_delete=models.CASCADE, related_name='brands')
    features = models.ManyToManyField(Feature, through='ProductFeature')
    slug =  models.SlugField(max_length=200,null=True)
    #------------------------------------------------
    def __str__(self):
        return self.product_name
        
    #------------------------------------------------
    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"slug": self.slug})
    #------------------------------------------------
    ##برای نمایش تخفیف کنار هر یک از کالاها
    def get_price_by_discount(self):
        list1 = []
        for dbd in self.discount_baskets_detalis2.all():
            if (dbd.discount_basket.is_active==True and 
                dbd.discount_basket.start_date <= datetime.now() and 
                datetime.now() <=  dbd.discount_basket.end_date):
                list1.append(dbd.discount_basket.discount)
        discount = 0
        if (len(list1)>0):
            discount = max(list1)
        return self.price - (self.price*discount/100)
 
    class Meta:
        verbose_name = ("کالا")
        verbose_name_plural =("کالا ها")
    #---------------------------------------------------------------------------------------------
    ##تعداد موجودی کالا درانبار
    def get_number_in_warehouse(self):
        sum1 = self.warehouses_prouduct.filter(warehouse_type_id = 1).aggregate(Sum('qty'))
        sum2 = self.warehouses_prouduct.filter(warehouse_type_id = 2).aggregate(Sum('qty'))#الباقی نوع انبار مصل مرجوعی -امانت گرفتن و دادن به همین شکل اضافه می کنیم 
        input = 0
        if sum1 ['qty__sum'] != None :
            input = sum1['qty__sum']
        output = 0
        if sum2['qty__sum'] != None :
            output = sum2['qty__sum']
        return input - output
  #----------------------------------------------------------------
    #--------------------------------------
    ## some scores are for any production that is  having user 
    def get_user_score(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score = user_score[0].score  
        return score 

    #--------------------------------------
    ## create avg function for any product with score
    def get_average_score(self):
        avgScore = self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore == None :
            avgScore = 0
        return avgScore
    #----------------------------------------------------------------
    ## is it product favorite   userّs or No
    def get_user_favorite(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        flag = self.favorite_product.filter(favorite_user=request.user).exists()
        return flag
    #----------------------------------------------------------------
    ##A function to return the commodity group=تابعی برای برگرداندن گروه کالا
    def getMainProductGroups(self):
        return self.product_group.all()[0].id 
    class Meta:
        verbose_name = 'کالا' 
        verbose_name_plural = 'کالاها'        

#---------------------------------------------------------------------------------------------
## create class FeatureValue
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=50, verbose_name='مقدار ویژگی')
    feature = models.ForeignKey(Feature, verbose_name=("ویژگی"), on_delete=models.CASCADE, related_name='feature_value')

    def __str__(self):  
        return f"{self.id}  {self.value_title}"
    class Meta:
        verbose_name = ("مقدار ویژگی ")
        verbose_name_plural =("مقدار های ویژگی  ")
#---------------------------------------------------------------------------------------------
## create class productFeature
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, verbose_name=("کالا"), on_delete=models.CASCADE,related_name='product_features')
    feature = models.ForeignKey(Feature, verbose_name=("ویژگی "), on_delete=models.CASCADE)
    value = models.CharField( max_length=100, verbose_name='مقدار ویژکی کالا')
    filter_value = models.ForeignKey(FeatureValue, null=True, blank=True, verbose_name="مقدار ویژگی برای فیلتر", on_delete=models.CASCADE,)
    def __str__(self) -> str:
        return f"{self.product}  - {self.feature} : {self.value}" 
    class Meta:
        verbose_name = ("ویژکی محصول")
        verbose_name_plural =("ویژگی های محصولات")
#---------------------------------------------------------------------------------------------
## create class productGallery
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name=("کالا"), on_delete=models.CASCADE,related_name='gallery_product')
    file_upload = FileUpload('images', 'ProductGallery')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر  کالا')
    class Meta:
        verbose_name = ("تصویر ")
        verbose_name_plural =('تصاویر')
#----------------------------------------------------------------
## create the def signala for the delete_product_image(1)
# def delete_product_image(sender, **kwargs):
#     print(100*"*")
#     print("prudelete_product_image...")
#     print(100*"*")
# post_delete.connect(receiver=delete_product_image, sender=Product)

## create the def signala for the delete_product_image(2)

@receiver(post_delete, sender=Product)
def delete_product_image(sender, **kwargs):
    print(100*"*")
    print("prudelete_deleted_image...")
    print(100*"*")