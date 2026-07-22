from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
      path ('cheapest_product/',get_cheapest_product,name='cheapest_product'),
      path ('last_product/',get_last_product,name='last_product'),
      path ('popular_product_groups/',get_popular_product_groups,name='popular_product_groups'),
      path ('product_details/<slug:slug>/',productDetaileView.as_view(),name='product_details'),
      path ('related_products/<slug:slug>/',get_related_products,name='related_products'),
      path ('product_groups/',ProductGroupView.as_view(),name='product_groups'),
      path ('product_of_group/<slug:slug>/',ProductsBygroupView.as_view(),name='product_of_group'),
      path ('ajax_admin/',get_filter_value_for_feature,name='filter_value_for_feature'),
      path ('product_groups_partial/',get_product_groups,name='product_groups_partial'),
      path ('ProductsBygroup/<slug:slug>/',ProductsBygroupView.as_view(),name='ProductsBygroup'),
      path ('brands_partial/<slug:slug>/',get_brands,name='brands_partial'),
      path ('ShowCompareListView/',ShowCompareListView.as_view(),name='ShowCompareListView'),
      path ('compare_table/',compare_table,name='compare_table'),
      path ('status_of_compare_list/',status_of_compare_list,name='status_of_compare_list'),
      path ('status_of_favorite_list/',status_of_favorite_list,name='status_of_favorite_list'),
      path ('add_to_compare_list/',add_to_compare_list,name='add_to_compare_list'),
      path ('delete_from_compare_list/',delete_from_compare_list,name='delete_from_compare_list'),
      path ('features_for_filter/<slug:slug>/',get_feature_for_filter,name='features_for_filter'),
]
