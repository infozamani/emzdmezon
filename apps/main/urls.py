from django.urls import path
from .views import index,SliderView,AboutUsView
app_name = 'main'
urlpatterns = [
    path('',index,name='index'),
    path('sliders/',SliderView.as_view(),name='sliders'),
    path('about_us/',AboutUsView.as_view(),name='about_us'),
  
]
