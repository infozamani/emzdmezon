from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import Slider
from .models import Slider,AboutUs,Post
#----------------------------------------------------------------
def media_admin(request):
    return {'media_url':settings.MEDIA_URL,}
#----------------------------------------------------------------
def index (request):
    return render(request,'main_app/index.html')

#----------------------------------------------------------------
class SliderView(View):
     def get(self, request):
         sliders = Slider.objects.filter(is_active=True)
         return render(request,'main_app/sliders.html',{'sliders':sliders})
#----------------------------------------------------------------
# show page 404
def handler404(request, exception=None):
    return render(request,'main_app/error404.html')

##about-us
class AboutUsView(View):
    def get(self, request):
        abouts = AboutUs.objects.all()
        print(abouts)
      
        return render(request,'main_app/about-us.html',{'abouts':abouts, })
#----------------------------------------------------------------
##context_us
def create_post(request):  
    if request.method == 'POST':  
        form = PostForm(request.POST)  
        if form.is_valid():  
            form.save()  # همچنین می‌توانید مستقیماً استفاده کنید.  
            messages.success(request,"پست با موفقیت ارسال شد")
            return redirect("main:index")  # یا هر URL دیگری که مدنظرتان است 
    else:   
        form = PostForm()  # برای نمایش فرم خالی  

    context = {  
        "form": form,
    }  
  
    return render(request, 'main_app/context_us.html', context)  