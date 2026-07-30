from django.shortcuts import render, get_object_or_404  
from django.http import Http404, HttpResponse
from django.template import loader
from .models import Author, Blog
from django.conf import settings
from django.views.generic.edit import CreateView
import os
from .forms import BlogForm
from django.core.files.storage import FileSystemStorage
import datetime


def blog(request):
    blogs = Blog.objects.filter(is_active=True)  # فقط مقالات فعال
    authors = Author.objects.all()
    latest_blogs = Blog.objects.filter(is_active=True).order_by('-id')[:6]

    context = {
        'blogs': blogs,
        'authors': authors,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'blog_app/blog.html', context)


def post_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, is_active=True)  # فقط مقالات فعال
    return render(request, 'blog_app/post_blog.html', {'blog': blog})


def showAuthors(request):
    authors = Author.objects.all()
    context = {
        'media_url': settings.MEDIA_URL,
        'authors': authors,
    }
    return render(request, 'blog_app/Author.html', context)


def author_detail(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        raise Http404("این صفحه یافت نشد")
    context = {
        'media_url': settings.MEDIA_URL,
        'author': author,
    }
    return render(request, 'blog_app/Author_detail.html', context)


# ================================================================
# ارسال ایمیل
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

def sendEmail(subject, message, to):
    email_form = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_form, to)


def sendEmail2(subject, message, html_content, to):
    email_form = settings.EMAIL_HOST_USER
    message = EmailMultiAlternatives(subject, message, email_form, to)
    message.attach_alternative(html_content, "text/html")
    message.send()


# ================================================================
# ایجاد مقاله جدید
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            imageupload = request.FILES['main_image']
            if imageupload.size < 10000:
                if imageupload.content_type == "image/jpeg" or imageupload.content_type == "image/png":
                    imgName, ext = os.path.splitext(imageupload.name)
                    currenttime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
                    imagepath = 'images/blogimg/' + imgName + currenttime + ext

                    data = form.cleaned_data
                    blog = Blog()
                    blog.title = data['title']
                    blog.description = data['description']
                    blog.summery_description = data.get('summery_description', '')
                    blog.is_active = data['is_active']
                    blog.author = data['author']
                    blog.main_image = imagepath
                    blog.save()

                    fss = FileSystemStorage()
                    fss.save(imagepath, imageupload)

                    # ارسال ایمیل
                    email_body = "<h1 style='color:red;'>مقاله با موفقیت درج شد</h1>"
                    sendEmail2(email_body, "", "ذخیره مقاله", ['emzimezon499@gmail.com'])

                    return render(request, 'blog_app/index.html')
                else:
                    context = {
                        "form": form,
                        'message': 'پسوند فایل را بررسی کنید (فقط jpeg و png مجاز است)',
                    }
            else:
                context = {
                    "form": form,
                    'message': 'سایز فایل باید کمتر از 10 کیلوبایت باشد',
                }
    else:
        form = BlogForm()
        context = {
            "form": form,
        }
    return render(request, 'blog_app/Blog_form.html', context)


# ================================================================
# تابع دریافت مقالات برای نمایش در اسلایدر (ایندکس)
def get_latest_blogs(request):
    """دریافت 6 مقاله آخر برای نمایش در اسلایدر ایندکس"""
    latest_blogs = Blog.objects.filter(is_active=True).order_by('-id')[:6]
    return render(request, 'partials/latest_blogs_slider.html', {'latest_blogs': latest_blogs})