from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# ------------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repassword",widget=forms.PasswordInput)
    class Meta :
        model  = CustomUser
        fields = ['mobile_number','email','name','family','gender']
        #کنترل پسورد
        def clean_password2(self):
            pass1 = self.cleaned_data["password1"]
            pass2 = self.cleaned_data["password2"]  
            if pass1 and pass2 and pass1 != pass2 :
                raise ValidationError('پسورد وارد شده با هم مغایرت دارد')
            return pass2
        # ----------------------------------------
        def save(self,commit = True):
            user = super().save(commit = False)#قبل از هش کردن سیو نکن 
            user.set_password(self.cleaned_data['password'])
            if commit :
                user.save()
            return user
# ----------------------------------------
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = 'برای تغییر رمز عبور روی <a href = "../password">   کلیک   </a>کیلیک کنید.')
    class Meta :
        model = CustomUser
        fields = ['mobile_number','password','email','name','family','gender','is_active','is_admin']
    
# ------------------------------------------------------------------------------------------
class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label="رمز عبور ",widget=forms.PasswordInput(attrs={'class' : "form-control" , 'placeholder' : 'رمزعبور را وارد کنید'}))
    password2 = forms.CharField(label="تکرار رمز عبور",widget=forms.PasswordInput(attrs={'class' : "form-control" , 'placeholder' : 'تکرار رمز عبور را وارد کنید'}))
    
    class Meta:
        model  = CustomUser
        fields = ['mobile_number']
        widgets = {
            'mobile_number':forms.TextInput(attrs={'class' : "form-control" , 'placeholder' : 'موبایل را وارد کنید'})}
        def clean_password2(self):
            pass1 = self.cleaned_data["password1"]
            pass2 = self.cleaned_data["password2"]  
            if pass1 and pass2 and pass1 != pass2 :
                raise ValidationError('پسورد وارد شده با هم مغایرت دارد')
            return pass2
#---------------------------------------------------------------------
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.TextInput(attrs={'class' : "form-control" , 'placeholder' : '   کد دریافتی را وارد کنید  '}))      
#---------------------------------------------------------------------
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل ',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.TextInput(attrs={'class' : "form-control" , 'placeholder' : '    موبایل را وارد کنید  '}))      
       
    password = forms.CharField(label='رمز عبور',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.PasswordInput(attrs={'class' : "form-control" , 'placeholder' : '    رمز عبور را وارد کنید  '}))      
#---------------------------------------------------------------------
#create change password form
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.PasswordInput(attrs={'class' : "form-control" , 'placeholder' : '    رمز عبور را وارد کنید  '}))      
    password2 = forms.CharField(label='تکراررمز عبور',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.PasswordInput(attrs={'class' : "form-control" , 'placeholder' : '    رمز عبور را وارد کنید  '}))      
    def clean_password2(self):
            pass1 = self.cleaned_data["password1"]
            pass2 = self.cleaned_data["password2"]  
            if pass1 and pass2 and pass1 != pass2 :
                raise ValidationError('پسورد وارد شده با هم مغایرت دارد')
            return pass2   

#---------------------------------------------------------------------
#create remember password form
class RrememberPasswordForm(forms.Form):
      mobile_number = forms.CharField(label='شماره موبایل ',
            error_messages = {"required": 'این فیلد نمی تواند خالی باشد'},
            widget = forms.TextInput(attrs={'class' : "form-control" , 'placeholder' : '    موبایل را وارد کنید  '}))      
#----------------------------------------------------------------
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={'class': "form-control" ,'placeholder':'شماره موبایل را وارد کنید', 'readonly':'readonly'})),
    name = forms.CharField(label="",
                             error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                             widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':'نام خود را وارد کنید'})),
    family = forms.CharField(label="",
                             error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                             widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':'نام خانوادگی  خود را وارد کنید'})),
    email = forms.EmailField(label="",
                             error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder':'ایمیل خود را وارد کنید'})),
    phon_number = forms.CharField(label="",
                             error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                             widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':'تلفن ثابت خود را وارد کنید'})),
    address = forms.CharField(label="",
                             error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                             widget=forms.Textarea(attrs={'class': "form-control", 'laceholder':'آدرس خود را وارد کنید'})),
    image = forms.ImageField(required=False)