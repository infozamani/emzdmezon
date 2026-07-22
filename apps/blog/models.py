from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField#تمام ابزار های ورد را نمایش میده


class Author (models.Model):
    name = models.CharField(max_length=30,verbose_name='نام')
    family = models.CharField(max_length=30,verbose_name='نام خانوادگی')
    slug = models.SlugField(max_length=30)
    age = models.IntegerField(default=30,verbose_name='سن')
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')
    register_data = models.DateTimeField(default=timezone.now,verbose_name='تاریخ ')
    email = models.EmailField(max_length=100,verbose_name='ایمیل')
    image_name= models.CharField(default='nophpont.png', blank=True ,null=True, max_length=200,verbose_name='تصویر')
    
    def __str__(self):
        return f"{self.name}\t{self.family}\t{self.age}\t{self.email}\t{self.image_name}" 
    #================================================================
    ## create savefile img and files
    
class Blog(models.Model):
        author = models.ForeignKey(Author, verbose_name=("نویسنده"), on_delete=models.CASCADE, related_name='authors')
        title = models.CharField(verbose_name = 'عنوان مقاله ', max_length=50)
        summery_description = models.TextField(default="",blank=True, null=True, verbose_name=' متن مقاله ')
        description = RichTextUploadingField(config_name = 'special',blank= None,verbose_name = ' توضیحات بیشتر درباره مقاله ')
        is_active = models.BooleanField(verbose_name = 'فعال /غیرفعال')
        main_image = models.ImageField(upload_to='images/blogimg', height_field=None, width_field=None,verbose_name = 'تصویر اصلی مقاله ')
       
        def __str__(self) -> str:
           return f"{self.title}\t{self.is_active}" 