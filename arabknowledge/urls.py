from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import HomeSitemap, CountrySitemap, ArticleSitemap, CategorySitemap
from articles import views
from django.views.static import serve  # استيراد serve لملفات جذر المشروع

# تعريف جميع الـ Sitemaps (استخدام الكائنات)
sitemaps = {
    'home': HomeSitemap(),
    'countries': CountrySitemap(),
    'articles': ArticleSitemap(),
    'categories': CategorySitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sitemap رئيسي لكل الموقع مع دومين محدد
  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),


    # Sitemap خاص بالدول (اختياري)
    path('sitemap/<slug:country_slug>.xml', views.country_sitemap, name='country_sitemap'),

    # دعم i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # روابط المقالات والدول
    path('', include('articles.urls')),

    # لوحة التحكم
    path('dashboard/', include('dashboard.urls')),

    # ملف robots.txt من جذر المشروع
    re_path(r'^robots\.txt$', serve, {
        'path': 'robots.txt',
        'document_root': settings.BASE_DIR,
        'show_indexes': False
    }),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# إعداد ملفات الوسائط (MEDIA) وملفات static أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
