from django.urls import path
from .views import *

app_name = 'csf'

urlpatterns = [
    path('create_comment/<slug:slug>/', CommantView.as_view(), name='create_comment'),
    path('add_score/', add_score, name='add_score'),
    path('add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/', remove_from_favorite, name='remove_from_favorite'),  # ✅ اضافه شد
    path('user_favorite/', UserFavoriteView.as_view(), name='user_favorite'),
]