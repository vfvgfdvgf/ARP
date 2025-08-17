from django.contrib.sitemaps import Sitemap
from .models import Country, Category, Article

class CountrySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Country.objects.all()

    def location(self, obj):
        return f'/{obj.slug}/'  # رابط الصفحة الرئيسية لكل دولة


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f'/{obj.country.slug}/category/{obj.slug}/'


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return f'/{obj.country.slug}/article/{obj.slug}/'
