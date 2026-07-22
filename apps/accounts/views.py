from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import RrememberPasswordForm,UpdateProfileForm,RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePasswordForm
import utils
from .models import CustomUser, Customer
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin#برای اینکه در خط آدرس اگر خط آدرس را بدهیم صفحه باز نشود
from django.core.exceptions import ObjectDoesNotExist
from apps.orders.models import Order
from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required


# ================================================================
# ثبت‌نام کاربر
# ================================================================
class RegisterUserView(View):
    template_name = 'account_app/register.html'
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            # دریافت فیلدها
            mobile_number = data.get('mobile_number', '').strip()
            name = data.get('name', '').strip()
            family = data.get('family', '').strip()
            email = data.get('email', '').strip()
            gender = data.get('gender', True)
            password = data.get('password1', '')
            
            # اعتبارسنجی شماره موبایل
            if not mobile_number:
                messages.error(request, 'شماره موبایل الزامی است', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی وجود شماره موبایل
            if CustomUser.objects.filter(mobile_number=mobile_number).exists():
                messages.error(request, 'این شماره موبایل قبلاً ثبت شده است', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی تطابق رمز عبور
            password2 = data.get('password2', '')
            if password != password2:
                messages.error(request, 'رمز عبور و تکرار آن مطابقت ندارند', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی طول رمز عبور
            if len(password) < 8:
                messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # ایجاد کد فعال‌سازی
            active_code = utils.create_random_code(5)
            
            # ایجاد کاربر
            try:
                user = CustomUser.objects.create_user(
                    mobile_number=mobile_number,
                    email=email,
                    name=name,
                    family=family,
                    active_code=active_code,
                    gender=gender,
                    password=password,
                )
                
                # ایجاد پروفایل Customer
                Customer.objects.create(user=user)
                
                # ارسال پیامک (اختیاری - اگر خطا داد ادامه بده)
                try:
                    utils.send_sms(mobile_number, active_code)
                except:
                    pass  # اگر پیامک ارسال نشد، خطا نده
                
                # نمایش کد در کنسول (برای تست)
                print(f"========== کد فعال‌سازی ==========")
                print(f"شماره: {mobile_number}")
                print(f"کد: {active_code}")
                print(f"====================================")
                
                # ذخیره در سشن
                request.session['user_session'] = {
                    'active_code': str(active_code),
                    'mobile_number': mobile_number,
                    'remember_password': False
                }
                
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد. کد فعال‌سازی را وارد کنید', 'success')
                return redirect('accounts:verify')
                
            except Exception as e:
                messages.error(request, f'خطا در ثبت‌نام: {str(e)}', 'danger')
                return render(request, self.template_name, {'form': form})
        
        # اگر فرم معتبر نبود
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', 'danger')
            
            messages.error(request, 'خطا در انجام ثبت‌نام. لطفاً اطلاعات را بررسی کنید', 'danger')
            return render(request, self.template_name, {'form': form})


class VerifyRegisterCodeView(View):
        #در خط آدرس اگر یوزر فعال بود هرچی وارد کند پرت کند به صفحه اصلی
    def dispatch(self, request, *args: Any, **kwargs: Any) :
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = VerifyRegisterForm()
        return render(request,'account_app/verify_regester_code.html',{'form':form})
    
    def post (self,request,*args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid() :
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code'] :
                user = CustomUser.objects.get(mobile_number = user_session ['mobile_number'] )
                if user_session['remember_password'] == False :
                    user.is_active   = True
                    user.active_code = utils.create_random_code(5) 
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد', 'succsses')
                    return redirect('main:index')
                else:
                    return redirect('accounts:change_pass')
            else:
                messages.error(request,'کد فعال سازی وارد شده اشتباه می باشد.', 'danger')
                return render(request,'account_app/verify_regester_code.html',{'form':form})
        messages.error(request,'اطلاعات وارد شده معتبر نمی باشد.', 'danger')
        return render(request,'account_app/verify_regester_code.html',{'form':form})
# -----------------------------------------------------------------------------------
#در خط آدرس اگر یوزر فعال بود هرچی وارد کند پرت کند به صفحه اصلی
class loginUserView(View):
    template_name = 'account_app/login.html'
    def dispatch(self, request, *args: Any, **kwargs: Any) :
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = LoginUserForm()
        return render(request,self.template_name,{'form':form})
    #--------------------------------------
    def post(self,request,*args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username = data['mobile_number'], password = data['password'])
            if user is not None :
                db_user = CustomUser.objects.get(mobile_number = data['mobile_number'])
                if db_user.is_admin == False :
                    messages.success(request,'ورود با موفقیت وارد شد.','success')
                    login(request,user)
                    next_url = request.GET.get('next ')
                    if next_url is not  None :
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                else:
                    messages.error(request,'کاربر ادمین نمی تواند وارد شود.','danger')
                    return render(request,self.template_name,{'form':form})

            else:
                messages.error(request,'اطلاعات وارد شده صحیح نمی باشد.','danger')
                return render(request,self.template_name,{'form':form})
        else:
            messages.error(request,'اطلاعات وارد شده نامعتبر است','danger')
            return render(request,self.template_name,{'form':form})
#------------------------------------------------------------------------------
##CREATE CLASS lOGOUT  #در خط آدرس اگر یوزر فعال بود هرچی وارد کند پرت کند به صفحه اصلی
class LogoutUserView(View):
    def dispatch(self, request, *args: Any, **kwargs: Any) :
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        session_data = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = session_data
        
        # messages.success(request,'خداحافظ')
        return redirect('main:index')
        
#------------------------------------------------------------------------------
##CREATE CLASS change password view
class ChangePasswordView(View):
    tempelate_name = 'account_app/change_password.html'
    
    def get(self,request,*args, **kwargs):
        form = ChangePasswordForm()
        return render(request,self.tempelate_name,{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = CustomUser.objects.get(mobile_number = user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code = utils.create_random_code(5)
            user.save()
            messages.success(request,'رمز شما با موفقیت تغییر کرد','success')
            return redirect('accounts:login')
        else:
            messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
            return render(request,self.tempelate_name,{'form':form})
            
#------------------------------------------------------------------------------
##CREATE CLASS rmember password view
class RememberPasswordView(View):
    tempelate_name = 'account_app/remember_password.html'
    def get(self,request,*args, **kwargs):
        form = RrememberPasswordForm()
        return render(request,self.tempelate_name,{'form':form})
    def post(self,request,*args, **kwargs):
        form = RrememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = CustomUser.objects.get(mobile_number = data['mobile_number'])
                active_code = utils.create_random_code(5)
                user.active_code = active_code
                user.save()
                #تابع ساخته شده برای اس ام اس
                utils.send_sms(data['mobile_number'],f'کدتایید شماره موبایل شما {active_code}می باشد '  )
                request.session ['user_session'] = {
                    'active_code' : str(active_code),
                    'mobile_number' : data['mobile_number'] ,
                    'remember_password':True,           
                }
                messages.success(request,'جهت تغییر رمز عبور خود کد دریافتی را ارسال نمایید','success')
                return redirect('accounts:verify')
            except:
                messages.error(request,'شماره موبایل وارد شده صحیح نمی باشد','danger')
                return render(request,self.tempelate_name,{'form':form})
#------------------------------------------------------------------------------
##CREATE CLASS USER PANEL
class UserPanelView(LoginRequiredMixin,View):
    def get(self,request ):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                "nmae" : user.name,
                "family" :user.family,
                "email" : user.email,
                "phone_number" : customer.phone_number,
                "address" : customer.address,
                "image" : customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info = {
                "phone_number" : customer.phone_number,
                "address" : customer.address,
                "image" : customer.image_name,
            }
        
        return render(request, 'account_app/userpanel.html', {"user_info"  : user_info})
#----------------------------------------------------------------
## نمایش سابقه پرداخت در پروفایل کاربرuserpanel
#برای اینکه حتما ماگین شده باشد چون تابع است از دیکیریتور استفاده می کنیم

@login_required
def show_last_orders(request):
    orders = Order.objects.filter(customer_id = request.user.id).order_by('-register_date')[:4]
    return render(request, 'account_app/partials/show_last_orders.html', {'orders': orders})
#----------------------------------------------------------------
@login_required
def show_user_payments(request):    
    payments = Payment.objects.filter(customer_id = request.user.id).order_by('-register_date')
    return render(request, 'account_app/show_user_payments.html', {'payments': payments})
#----------------------------------------------------------------
## تابع ویرایش پروفایل 
class UpdateProfileView(LoginRequiredMixin, View):
    def ger(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
            initial_dict = {
                "mobile_number" : user.mobile_number,
                "name" : user.name,
                "family" :user.family,
                "email" : user.email,
                "phone_number" : customer.phone_number,
                "address" : customer.address,
                
            }
        except ObjectDoesNotExist:
            initial_dict  = {
                "mobile_number" : user.mobile_number,
                "name" : user.name,
                "family" :user.family,
                "email" : user.email,
            }
            
        form = UpdateProfileForm(initial=initial_dict)
        return render(request, 'account_app/update_profile.html', {"form": form, "image_url": customer.image_name})
    
    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.name = cd['name']        
            user.family = cd['family']
            user.email = cd['email']
            user.save()
            try:
              customer = Customer.objects.get(user=request.user)
              customer.phone_number = cd['phone_number']
              customer.address = cd['address']
              customer.image_name = cd['image']
              customer.save()
            except ObjectDoesNotExist: 
              customer.objects.create(
                  user = request.user,
                  phone_number = cd['phone_number'],
                  address = cd['address'],
                  image_name = cd['image']
              )
              messages.success(request,'ویرایش پروفایل با موفقیت انجام شد','success')
              return redirect('accounts:userpanel')
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger' )
            return render(request, 'main_app/update_profile.html',{'form':form}) 
        
        
        
         