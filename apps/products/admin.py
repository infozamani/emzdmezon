from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q  
from django.contrib.admin import SimpleListFilter
#این ماول برای فارسی کردن منوها و اوردر کردن
from admin_decorators import short_description,order_field ##pip install django-admin-decorators
from django_admin_listfilter_dropdown.filters import  DropdownFilter###pip install django-admin-list-filter-dropdownدر ستینگ هم اضافه شود

#-------------------------------------------------------------------------
#create class for Column group_parent and persion and updete
#-------------------------
##actionsبرای این که دیگر برانامه مجزا ننویسیم تابع ای می نویسیم و آن را به کلاس اضافه می کنیم خط 72نگاه کنید.
def de_active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active = False)
    message = f'تعداد گروه {res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-------------------------------------------------------------------------    
def active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active = True)
    message = f'تعدادگروه{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-------------------------------------------------------------------------
## create export_file json  برای استخراج ای پی ای از این تابه استفاده می کنیم خط72 
def export_json(modeladmin,request,queryset):
    response = HttpResponse(content_type = 'application/json')
    serializers.serialize("json",queryset,stream = response)
    return response
    
    
#-------------------------------------------------------------------------
## create sub_group    
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 1
#-------------------------------------------------------------------------
##craete filterGroupبرای فیلتر سازی شخصی استفاده می گردد
class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات ' 
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent = None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]
    
    def queryset(self, request, queryset) :
        if self.value()!= None:
            return queryset.filter(Q(group_parent = self.value()))
        return queryset
#-------------------------------------------------------------------------
@ admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_dialects = ('brand_name',)
    list_filter = ('brand_name',)
    search_fields = ('brand_name',)
    ordering = ('brand_name',)
    

#-------------------------------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_date','update_date','count_sun_group','count_product_of_group')
    list_filter = (GroupFilter,('group_parent',DropdownFilter), 'is_active')
    search_fields = ('group_title',)
    ordering = ('group_title','group_parent')
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [de_active_product_group,active_product_group,export_json]
    list_editable = ['is_active']#for btn 
    #--------------------------------------------
    ##create Column products_of_groupsبرای ایجاد ستون در گروه کالاها
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
       qs = super(ProductGroupAdmin,self).get_queryset(*args, **kwargs)
       qs = qs.annotate(sub_group = Count('groups'))
       qs = qs.annotate(product_of_group = Count('products_of_groups'))
       return qs
    #--------------------------------------------
    def count_sun_group(self, object):
        return object.sub_group
    #--------------------------------------------
    ##  create pertion راه دوم  فارسی کردن سر ستونها
    @short_description('تعداد کالاهای گروه')
    @order_field('product_of_group')# کار اوردر را انجام میده 
    def count_product_of_group(self, object):
        return object.product_of_group
    
    #--------------------------------------------
    ##  create pertion برای فارسی کردن سر ستونها
    count_sun_group.short_description = 'تعداد زیر گروه ها'
    # count_product_of_group.short_description = 'تعداد کالا ها'
    de_active_product_group.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product_group.short_description = ' فعال کردن کالا های انتخاب شده'
    export_json.short_description = 'خروجی جیسونی از گروه انتخاب شده '
#-----------------------------------------------------------------------
def de_active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = False)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-----------------------------------------------------------------------   
def active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = True)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-----------------------------------------------------------------------
## create FeatuerInstance product
class ProductFeatureInstanceAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 3
    #==================================================
    class Media:
        css = {
            'all' :('css/admin_style.css',)
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',)
#-----------------------------------------------------------------------
## create save Similar gallery product
class ProductProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3
#-----------------------------------------------------------------------
## create save Similar feature value product
class FeatureValueInlineAdmin(admin.TabularInline):
    model = FeatureValue
    extra = 3
    
#-----------------------------------------------------------------------
## create Featureadmin
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','display_groups',  'display_freature_value')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInlineAdmin,]
    
     #--------------------------------------------
    ##create def formfield_for_manytomany(self, db_field, request, **kwargs):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent = None))
        return super().formfield_for_manytomany(db_field,request,**kwargs)
     #--------------------------------------------
    def display_groups(self,obj):
        return ','.join([group.group_title for group in obj.product_group.all()])
     #--------------------------------------------
    def display_freature_value(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
      
    
    display_groups.short_description = 'گروه ها دارای این ویژگی'
    display_freature_value.short_description = 'مقادیر ممکن برای این ویژگی' 
#-----------------------------------------------------------------------
## create FeatureValuAadmin
@admin.register(FeatureValue)
class FeatuerValueAdmin(admin.ModelAdmin):
    list_display =('value_title','feature')
    
    fieldsets = ((None,{'fields':('feature','value_title',)}),)
#-----------------------------------------------------------------------    
##create product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','display_product_groups','price','is_active','brand','update_date','slug',)
    # list_filter = ('brand','product_group')
    list_filter = (('brand__brand_name',DropdownFilter),('product_group__group_title',DropdownFilter),)
    search_fields = ('product_name',)
    ordering = ('update_date','product_name')
    actions = [de_active_product,active_product,]
    inlines = [ProductFeatureInstanceAdmin,ProductProductGalleryInlineAdmin]
    list_editable = ['is_active']
    de_active_product.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product.short_description = ' فعال کردن کالا های انتخاب شده'
     #--------------------------------------------
    # ##create Column for any object or fields
    def display_product_groups(self,obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    display_product_groups.short_description = 'گروه کالا'
    #----------------------------------------------
    ## create filter product null
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    #--------------------------------------------
## افقی کردن داشبورد پروداکت)(product)
    fieldsets = (
        ('اطلاعات محصولات',{'fields':(
        'product_name',
        'image_name',
        'price',
        ('product_group','brand','is_active'),
        'summery_description',
        'description',
        'slug',
        )}),
        ('تاریخ وزمان',{'fields':(
            'published_date',
             
        )}),
    )
    
    