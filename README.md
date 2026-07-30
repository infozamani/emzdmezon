📋 راهنمای جامع فروشگاه اینترنتی پوشاک ایزدمزون (EMZDMezon)
🎯 معرفی پروژه
ایزدمزون (EMZDMezon) یک فروشگاه اینترنتی تخصصی در حوزه پوشاک زنانه است که با استفاده از فریم‌ورک قدرتمند جنگو (Django) توسعه یافته است. این پروژه یک پلتفرم کامل و حرفه‌ای برای فروش آنلاین لباس‌های زنانه، اکسسوری‌ها و محصولات مرتبط با مد و فشن می‌باشد.

🛠️ تکنولوژی‌های استفاده شده
بخش	تکنولوژی
بک‌اند	Django 5.0.3
پایگاه داده	MySQL
فرانت‌اند	HTML5, CSS3, Bootstrap 4.5.3
جاوااسکریپت	jQuery, Owl Carousel
ویرایشگر متن	CKEditor
احراز هویت	Django Authentication
پرداخت	ZarinPal
فیلترسازی	Django Filters
API	Django REST Framework
📂 ساختار پروژه
text
emzdmezon/
├── manage.py
├── shop/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── main/           # اپ اصلی
│   │   ├── models.py   # Slider, AboutUs, Post
│   │   ├── views.py
│   │   └── urls.py
│   ├── products/       # اپ محصولات
│   │   ├── models.py   # Product, Brand, ProductGroup, Feature...
│   │   ├── views.py
│   │   └── urls.py
│   ├── accounts/       # اپ کاربران
│   ├── orders/         # اپ سفارشات
│   ├── discounts/      # اپ تخفیف‌ها
│   ├── payments/       # اپ پرداخت
│   ├── warehouses/     # اپ انبارداری
│   ├── blog/           # اپ وبلاگ
│   ├── comment_scoring_favorites/  # اپ نظرات، امتیازات و علاقه‌مندی‌ها
│   └── search/         # اپ جستجو
├── templates/
│   ├── partials/
│   └── main_template.html
├── static/
├── media/
└── middlewares/
📊 مدل‌های پایگاه داده
۱. اپ اصلی (main)
مدل Slider (اسلایدشو)
اسلایدهای نمایشی صفحه اصلی فروشگاه را مدیریت می‌کند.

فیلد	نوع	توضیح
slider_title1	CharField	متن اول اسلاید
slider_title2	CharField	متن دوم اسلاید
slider_title3	CharField	متن سوم اسلاید
image_title	ImageField	تصویر اسلاید
slider_link	URLField	لینک اسلاید
is_active	BooleanField	فعال/غیرفعال
مدل AboutUs (درباره ما)
محتوای صفحه درباره ما را مدیریت می‌کند.

فیلد	نوع	توضیح
about_title	CharField	عنوان
user_registered	ForeignKey	کاربر ثبت‌کننده
description	RichTextUploadingField	توضیحات کامل
image_title	ImageField	تصویر
مدل Post (پیام‌ها)
پیام‌های ارسالی از طریق فرم تماس را ذخیره می‌کند.

فیلد	نوع	توضیح
name	CharField	نام کاربر
title	CharField	موضوع
descriptions	TextField	متن پیام
email	EmailField	ایمیل کاربر
۲. اپ محصولات (products)
مدل Brand (برند)
مدیریت برندهای پوشاک.

فیلد	نوع	توضیح
brand_name	CharField	نام برند
image_name	ImageField	لوگو برند
slug	SlugField	نامک برای SEO
مدل ProductGroup (دسته‌بندی)
دسته‌بندی سلسله‌مراتبی محصولات.

فیلد	نوع	توضیح
group_title	CharField	عنوان دسته‌بندی
image_name	ImageField	تصویر
group_parent	ForeignKey	دسته‌بندی والد
is_active	BooleanField	فعال/غیرفعال
slug	SlugField	نامک
مدل Product (محصول)
محصولات اصلی فروشگاه.

فیلد	نوع	توضیح
product_name	CharField	نام محصول
price	PositiveIntegerField	قیمت
description	RichTextUploadingField	توضیحات کامل
image_name	ImageField	تصویر اصلی
brand	ForeignKey(Brand)	برند
product_group	ManyToManyField	دسته‌بندی‌ها
features	ManyToManyField	ویژگی‌ها
is_active	BooleanField	فعال/غیرفعال
slug	SlugField	نامک
متدهای کاربردی:

get_price_by_discount(): محاسبه قیمت با تخفیف

get_number_in_warehouse(): محاسبه موجودی انبار

get_average_score(): میانگین امتیازات محصول

get_user_favorite(): بررسی علاقه‌مندی کاربر

مدل Feature (ویژگی)
ویژگی‌های محصولات مانند جنس، سایز، رنگ.

فیلد	نوع	توضیح
feature_name	CharField	نام ویژگی
product_group	ManyToManyField	دسته‌بندی مرتبط
مدل ProductFeature (ویژگی محصول)
اتصال ویژگی‌ها به محصولات با مقدار مشخص.

فیلد	نوع	توضیح
product	ForeignKey	محصول
feature	ForeignKey	ویژگی
value	CharField	مقدار
۳. اپ نظرات و امتیازات (comment_scoring_favorites)
مدل Comment (نظر)
مدیریت نظرات کاربران.

فیلد	نوع	توضیح
product	ForeignKey	محصول
commenting_user	ForeignKey	کاربر نظردهنده
comment_text	TextField	متن نظر
is_active	BooleanField	تایید/عدم تایید
comment_parent	ForeignKey	پاسخ به نظر
مدل Scoring (امتیاز)
امتیازدهی کاربران به محصولات.

فیلد	نوع	توضیح
product	ForeignKey	محصول
scoring_user	ForeignKey	کاربر
score	PositiveIntegerField	امتیاز (۰ تا ۵)
مدل Favorite (علاقه‌مندی)
لیست محصولات مورد علاقه کاربران.

فیلد	نوع	توضیح
product	ForeignKey	محصول
favorite_user	ForeignKey	کاربر
۴. اپ وبلاگ (blog)
مدل Author (نویسنده)
مدیریت نویسندگان مقالات.

فیلد	نوع	توضیح
name	CharField	نام
family	CharField	نام خانوادگی
email	EmailField	ایمیل
is_active	BooleanField	فعال/غیرفعال
مدل Blog (مقاله)
مدیریت مقالات وبلاگ.

فیلد	نوع	توضیح
author	ForeignKey	نویسنده
title	CharField	عنوان
description	RichTextUploadingField	متن کامل
main_image	ImageField	تصویر اصلی
is_active	BooleanField	فعال/غیرفعال
🎨 رابط کاربری و تم‌ها
پروژه از تم آبی-صورتی حرفه‌ای استفاده می‌کند که شامل رنگ‌های زیر است:

css
--blue-deep: #1E3A8A;     /* آبی تیره */
--blue-primary: #3B82F6;   /* آبی اصلی */
--pink-accent: #EC4899;    /* صورتی */
--purple-mix: #8B5CF6;     /* بنفش */
--glass-bg: rgba(255,255,255,0.75);  /* افکت شیشه‌ای */
ویژگی‌های ظاهری:

✅ افکت شیشه‌ای (Glassmorphism)

✅ انیمیشن‌های نرم و حرفه‌ای

✅ واکنش‌گرا (Responsive) برای تمام دستگاه‌ها

✅ آیکون‌های FontAwesome

✅ کاروسل‌های Owl Carousel

🚀 قابلیت‌های اصلی سیستم
۱. مدیریت محصولات
ایجاد، ویرایش و حذف محصولات

دسته‌بندی سلسله‌مراتبی

ویژگی‌های متنوع (سایز، رنگ، جنس)

گالری تصاویر چندگانه

برندهای مختلف

۲. سیستم تخفیف و قیمت‌گذاری
تخفیف‌های درصدی و مبلغی

قیمت‌های ویژه برای مناسبت‌ها

نمایش خودکار قیمت با تخفیف

۳. مدیریت انبار
موجودی دقیق محصولات

ورود و خروج کالا

نمایش موجودی به کاربران

۴. نظرات و امتیازات
ثبت نظر برای محصولات

امتیازدهی ۱ تا ۵ ستاره

پاسخ به نظرات کاربران

۵. علاقه‌مندی‌ها
ذخیره محصولات مورد علاقه

دسترسی سریع از پنل کاربری

۶. سبد خرید و سفارشات
افزودن/حذف محصولات

تغییر تعداد

محاسبه خودکار قیمت

پیگیری سفارشات

۷. پرداخت آنلاین
اتصال به درگاه زرین‌پال

پرداخت امن

تایید خودکار پرداخت

۸. وبلاگ
مقالات آموزشی و خبری

دسته‌بندی مقالات

نمایش در صفحه اصلی و صفحه بلاگ

۹. جستجوی پیشرفته
جستجو بر اساس نام، برند، دسته‌بندی

فیلترهای متعدد (قیمت، برند، ویژگی‌ها)

مرتب‌سازی (قیمت، جدیدترین، محبوب‌ترین)

۱۰. پنل کاربری
مشاهده و ویرایش پروفایل

تاریخچه سفارشات

لیست علاقه‌مندی‌ها

مدیریت نظرات

📱 صفحات اصلی سایت
صفحه	توضیح
خانه (Index)	اسلایدشو، محصولات ویژه، دسته‌بندی‌ها، مقالات
محصولات	لیست محصولات با فیلتر و مرتب‌سازی
جزئیات محصول	تصاویر، قیمت، ویژگی‌ها، نظرات، امتیاز
سبد خرید	لیست محصولات، ویرایش تعداد، محاسبه قیمت
پرداخت	اطلاعات ارسال، انتخاب درگاه، پرداخت
وبلاگ	لیست مقالات، جستجو، دسته‌بندی
جزئیات مقاله	متن کامل مقاله، نویسنده، تاریخ
درباره ما	اطلاعات فروشگاه
تماس با ما	فرم ارسال پیام
پنل کاربری	مدیریت حساب کاربری
🔒 امنیت سیستم
✅ احراز هویت کاربران (ورود/ثبت‌نام)

✅ تایید نظرات قبل از انتشار

✅ CSRF Protection

✅ رمزنگاری پسوردها

✅ مدیریت دسترسی‌ها

✅ محافظت در برابر حملات XSS و SQL Injection

📦 نصب و راه‌اندازی
bash
# ۱. کلون کردن پروژه
git clone https://github.com/yourusername/emzdmezon.git
cd emzdmezon

# ۲. ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# ۳. نصب وابستگی‌ها
pip install -r requirements.txt

# ۴. تنظیمات پایگاه داده
# فایل shop/settings.py را ویرایش کنید

# ۵. اعمال migration‌ها
python manage.py makemigrations
python manage.py migrate

# ۶. ایجاد کاربر ادمین
python manage.py createsuperuser

# ۷. جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic

# ۸. اجرای سرور
python manage.py runserver
📧 اطلاعات توسعه‌دهنده
مورد	توضیح
نام سازنده	فریبرز زمانی (Fariborz Zamani)
ایمیل	fariborz499@gmail.com
نام فروشگاه	ایزدمزون (EMZDMezon)
نوع فروشگاه	پوشاک زنانه آنلاین
تکنولوژی	Django 5, MySQL, Bootstrap 4
سال توسعه	۱۴۰۴ (۲۰۲۵)
🌟 نتیجه‌گیری
پروژه ایزدمزون یک فروشگاه اینترنتی کامل و حرفه‌ای برای فروش پوشاک زنانه است که با استفاده از بهترین تکنولوژی‌های روز دنیا توسعه یافته است. این سیستم با داشتن امکانات کامل مدیریت محصولات، سفارشات، پرداخت، وبلاگ و نظرات، یک پلتفرم جامع برای کسب‌وکارهای آنلاین حوزه مد و فشن محسوب می‌شود.