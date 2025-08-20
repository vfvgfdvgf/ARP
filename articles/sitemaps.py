from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Country, Category

# ---------------- الصفحة الرئيسية ----------------
class HomeSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'  # يستخدم البروتوكول عند توليد الروابط

    def items(self):
        return ['home']  # اسم URL name للصفحة الرئيسية

    def location(self, item):
        return reverse(item)  # رابط نسبي فقط


# ---------------- صفحات الدول ----------------
class CountrySitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return Country.objects.all()

    def location(self, obj):
        return reverse('country_home', args=[obj.slug])


# ---------------- المقالات ----------------
class ArticleSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('article_detail', args=[obj.country.slug, obj.slug])


# ---------------- التصنيفات ----------------
class CategorySitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_view', args=[obj.country.slug, obj.slug])
