from django.urls import path
import apps.blog.views as views
from .views import *

app_name = 'blogs'
urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('post_blog/<int:blog_id>/', views.post_blog, name='post_blog'),
    path('blog1/', views.showAuthors, name='blog1'),
    path('blog2/', views.create_blog, name='blog2'),
    path('blog3/<int:author_id>', views.author_detail, name='blog3'),
    path('latest-blogs/', views.get_latest_blogs, name='latest_blogs'),
]