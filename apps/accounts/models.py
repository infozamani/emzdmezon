from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from utils import FileUpload
from django.utils import timezone
#2=============================================================================
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,email="",name="",family="",active_code=None,gender=True,password = True):
        if not mobile_number :
            raise ValueError('شماره موبایل باید وارد کنید')
        user = self.model(
            mobile_number  = mobile_number,
            email          = self.normalize_email(email),
            name           = name,
            family         = family,
            active_code    = active_code,
            gender         = gender,
        )
        user.set_password(password)#برای هش کردن پسورد 
        user.save(using=self._db)
        return user
     # -----------------------------------------------------------
    def create_superuser(self,mobile_number,email,name,family,active_code=None,gender=True,password = True):
        user = self.create_user(
            mobile_number  = mobile_number,
            email          = email,
            name           = name,
            family         = family,
            active_code    = active_code,
            gender         = gender,
            password       = password,   
        ) 
        user.is_active    = True
        user.is_admin     = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#1=============================================================================
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number = models.CharField( max_length=11,unique= True,verbose_name='شماره موبایل')
    email         = models.EmailField(max_length=254,blank = True)
    name          = models.CharField(max_length=50,blank = True)
    family        = models.CharField(max_length=50,blank = True)
    GENDER_CHOICES= (('True','مرد'),('False','زن'))
    gender        = models.CharField(max_length=50,blank = True , choices = GENDER_CHOICES,default = True,null =True )
    register_data = models.DateField(default = timezone.now)
    is_active     = models.BooleanField(default = False)
    active_code   = models.CharField(max_length=100,null =True,blank = True)
    is_admin      = models.BooleanField(default = False)
  
    
    
    USERNAME_FIELD  = 'mobile_number'
    REQUIRED_FIELDS = ['email','name','family']
    
    objects = CustomUserManager()
    #----------------------------------
    def __str__(self):
        return self.name+" "+self.family
    

    #----------------------------------
    #کار بر را به ادمین ادمین کردن 
    @property
    def is_staff(self):
        return self.is_admin
    
#---------------------------------------------------------
## create class customer
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField( max_length=11, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    file_upload = FileUpload('images', 'customer')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name='تصویر پروفایل  ', null=True, blank=True)#برای اینکه فایل عمومی برای همه فیلد های مدل های مختلف داشته باشیم تابعی در پوشه مشترک می سازم 
    
    def __str__(self):
        return f"{self.user}"

