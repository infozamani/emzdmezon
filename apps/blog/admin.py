from django.contrib import admin
from .models import Author, Blog


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'age', 'register_data', 'is_active')
    search_fields = ('name', 'family')
    list_filter = ('is_active',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'register_data')
    list_filter = ('is_active', 'author')
    search_fields = ('title', 'summery_description')
    readonly_fields = ('register_data',)
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'author', 'summery_description', 'description', 'main_image')
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
    )