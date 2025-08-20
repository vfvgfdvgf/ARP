from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from articles.sitemaps import HomeSitemap, CountrySitemap, ArticleSitemap, CategorySitemap

sitemaps = {
    'home': HomeSitemap,
    'countries': CountrySitemap,
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.home_view, name='home'),

    # البحث العام
    path('search/', views.search_view, name='search_results'),

    # الصفحات التعريفية
    path('about/', views.about_view, name='about'),
    path('privacy-policy/', views.privacy_policy_main_view, name='privacy_policy'),
    path('terms/', views.terms_main_view, name='terms'),
    path('faq/', views.faq_view, name='faq'),

    # Sitemap الرئيسي
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # مسارات الدول والمقالات
    path('<slug:country_slug>/', views.country_home_view, name='country_home'),
    path('<slug:country_slug>/categories/', views.categories_view, name='categories'),
    path('<slug:country_slug>/category/<slug:category_slug>/', views.category_view, name='category_view'),
    path('<slug:country_slug>/article/<slug:article_slug>/', views.article_detail, name='article_detail'),
    path('<slug:country_slug>/about/', views.country_about_view, name='country_about'),
    path('<slug:country_slug>/contact/', views.country_contact_view, name='country_contact'),
    path('<slug:country_slug>/privacy-policy/', views.country_privacy_policy_view, name='country_privacy_policy'),
    path('<slug:country_slug>/terms/', views.country_terms_view, name='country_terms'),

    # بحث خاص بالدولة
    path('<slug:country_slug>/search/', views.search_view, name='country_search'),
]
