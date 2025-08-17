from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import CountrySitemap, CategorySitemap, ArticleSitemap
from articles import views

# تعريف جميع الـ Sitemaps (استخدام الصفوف وليس الكائنات)
sitemaps = {
    'countries': CountrySitemap(),
    'categories': CategorySitemap(),
    'articles': ArticleSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sitemap واحد لكل الموقع
    path('sitemap/<slug:country_slug>.xml', views.country_sitemap, name='country_sitemap'),

    # دعم i18n لإصلاح مشاكل set_language
    path('i18n/', include('django.conf.urls.i18n')),

    # روابط المقالات والدول
    path('', include('articles.urls')),

    # لوحة التحكم
    path('dashboard/', include('dashboard.urls')),

    # ملف robots.txt
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# إضافة ملفات الوسائط والستاتيك أثناء التطوير فقط
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
