from django.db import models
from  utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from apps.accounts.models import Customer

#----------------------------------------------------------------
## create a new class Slider 
class Slider(models.Model):
    slider_title1 = models.CharField(max_length= 500,null=True,blank=True,verbose_name="متن اول")
    slider_title2 = models.CharField(max_length= 500,null=True,blank=True,verbose_name="متن دوم")
    slider_title3 = models.CharField(max_length= 500,null=True,blank=True,verbose_name="متن سوم")
    file_upload = FileUpload('images','slides')
    image_title = models.ImageField(upload_to=file_upload.upload_to,verbose_name ='تصویر اسلاید')
    slider_link = models.URLField(max_length=200, blank=True, null=True,verbose_name='لینک')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='فعال/غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField( auto_now=True, verbose_name='آخرین ویرایش' )
    
    def __str__(self) -> str:
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدها'
    
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_title}" Style="width:80px;height:80px;border:1px solid"/>')
    image_slide.short_description = 'تصویر اسلاید'
    
    
    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">link</a>')
    link.short_description = '   پیوند ها'
## create a new class About_Us
class AboutUs(models.Model):
    about_title = models.CharField(max_length= 200,verbose_name=" عنوان متن") 
    user_registered = models.ForeignKey(Customer, verbose_name="کاربر", on_delete=models.CASCADE,related_name='about_us_Customuser')
    description = RichTextUploadingField(config_name = 'special',blank= None)
    file_upload = FileUpload('images','abouts')
    image_title = models.ImageField(upload_to=file_upload.upload_to,verbose_name ='تصویر اسلاید')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='فعال/غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField( auto_now=True, verbose_name='آخرین ویرایش' )
    
    def __str__(self) -> str:
        return f"{self.about_title}"
    
    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ماها'
#----------------------------------------------------------------
## create a new post 
class Post (models.Model):
    name = models.CharField(max_length=30,verbose_name="نام")
    title = models.CharField(max_length=30,verbose_name='موضوع  ')
    descriptions = models.TextField(max_length=3000,verbose_name='نظرات  ')
    email =models.EmailField( max_length=254,verbose_name='ایمیل')
    is_active = models.BooleanField(default=False,   verbose_name='فعال/غیرفعال')
    
    def __str__(self) -> str:
        return self.title+""+self.descriptions+""+str(self.is_active)
