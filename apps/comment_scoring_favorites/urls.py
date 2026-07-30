from django.urls import path
from .views import *

app_name = 'csf'
urlpatterns = [
    path('create_comment/<slug:slug>/', CommantView.as_view(), name='create_comment'),
    path ('add_to_favorite/',add_to_product_fvorite, name='add_to_favorite'),
    path('add_score/', add_score, name='add_score'),
    path('add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('user_favorite/', UserFavoriteView.as_view(), name='user_favorite'),
]
