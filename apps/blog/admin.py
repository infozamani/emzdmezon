from django.contrib import admin
from .models import Author,Blog


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','family','age','register_data','is_active')
 
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title' ,'is_active')
 