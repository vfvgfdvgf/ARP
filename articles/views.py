from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import ContactForm
from .models import Country, Category, Article, Comment

# ===============================================
# الصفحة الرئيسية - عرض قائمة الدول
# ===============================================
def home_view(request):
    countries = Country.objects.all()
    return render(request, 'articles/home.html', {'countries': countries})

# الصفحة الرئيسية لكل دولة
def country_home_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    articles = Article.objects.filter(country=country)
    categories = Category.objects.filter(country=country)
    return render(request, 'articles/country_home.html', {
        'country': country,
        'articles': articles,
        'categories': categories
    })

# ===============================================
# عرض المقالات حسب التصنيف
# ===============================================
def category_view(request, country_slug, category_slug):
    country = get_object_or_404(Country, slug=country_slug)
    category = get_object_or_404(Category, slug=category_slug, country=country)
    articles = Article.objects.filter(category=category)
    return render(request, 'articles/category_view.html', {
        'country': country,
        'category': category,
        'articles': articles
    })

# ===============================================
# تفاصيل المقالة + التعليقات
# ===============================================
def article_detail(request, country_slug, article_slug):
    country = get_object_or_404(Country, slug=country_slug)
    article = get_object_or_404(Article, slug=article_slug, country=country)

    # إضافة التعليق إذا كان الطلب POST
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        if not name or not content:
            messages.error(request, 'يرجى إدخال الاسم والتعليق.')
        else:
            Comment.objects.create(
                article=article,
                name=name,
                content=content,
                created_at=timezone.now()
            )
            messages.success(request, 'تم إضافة تعليقك بنجاح.')
            return redirect('article_detail', country_slug=country.slug, article_slug=article.slug)

    # عرض التعليقات
    comments = article.comments.all().order_by('-created_at')

    # مقالات ذات صلة (من نفس التصنيف إن وجد، وإلا من نفس الدولة)
    if article.category:
        related_articles = Article.objects.filter(
            category=article.category, country=country
        ).exclude(id=article.id)[:5]
    else:
        related_articles = Article.objects.filter(
            country=country
        ).exclude(id=article.id)[:5]

    return render(request, 'articles/article_detail.html', {
        'country': country,
        'article': article,
        'comments': comments,
        'related_articles': related_articles
    })

# ===============================================
# البحث
# ===============================================
from django.db.models import Q
from difflib import get_close_matches

def search_view(request, country_slug=None):
    query = request.GET.get('q', '').strip()
    country = None
    articles = []
    categories = []

    if query:
        # بحث بدولة محددة
        if country_slug:
            country = get_object_or_404(Country, slug=country_slug)

            # نتائج مباشرة
            articles = Article.objects.filter(country=country, title__icontains=query)
            categories = Category.objects.filter(country=country, name__icontains=query)

            # لو ما فيه نتائج → تقريبية
            if not articles.exists() and not categories.exists():
                all_titles = list(Article.objects.filter(country=country).values_list("title", flat=True))
                close_titles = get_close_matches(query, all_titles, n=5, cutoff=0.4)  # 0.4 = نسبة التشابه
                articles = Article.objects.filter(country=country, title__in=close_titles)

                all_cats = list(Category.objects.filter(country=country).values_list("name", flat=True))
                close_cats = get_close_matches(query, all_cats, n=5, cutoff=0.4)
                categories = Category.objects.filter(country=country, name__in=close_cats)

        # بحث عام (لو ما فيه دولة)
        else:
            articles = Article.objects.filter(title__icontains=query)
            categories = Category.objects.filter(name__icontains=query)

            if not articles.exists() and not categories.exists():
                all_titles = list(Article.objects.values_list("title", flat=True))
                close_titles = get_close_matches(query, all_titles, n=5, cutoff=0.4)
                articles = Article.objects.filter(title__in=close_titles)

                all_cats = list(Category.objects.values_list("name", flat=True))
                close_cats = get_close_matches(query, all_cats, n=5, cutoff=0.4)
                categories = Category.objects.filter(name__in=close_cats)

    return render(request, 'articles/search_results.html', {
        'country': country,
        'articles': articles,
        'categories': categories,
        'query': query
    })



# ===============================================
# عرض جميع التصنيفات لدولة معينة
# ===============================================
def categories_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    categories = Category.objects.filter(country=country)
    return render(request, 'categories.html', {
        'country': country,
        'categories': categories
    })

# ===============================================
# الصفحات التعريفية العامة للصفحة الرئيسية
# ===============================================
def about_view(request):
    return render(request, 'articles/about.html')

def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=f"المرسل: {form.cleaned_data['name']} - {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            return redirect('contact')
    return render(request, 'articles/contact.html', {'form': form})

def privacy_policy_main_view(request):
    return render(request, 'articles/privacy_policy.html')

def terms_main_view(request):
    return render(request, 'articles/terms.html')

def faq_view(request):
    return render(request, 'articles/faq.html')

def main_sitemap(request):
    return render(request, 'articles/main_sitemap.html')

# ===============================================
# الصفحات التعريفية لكل دولة
# ===============================================
def country_about_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    return render(request, 'articles/country_about.html', {'country': country})

def country_contact_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=f"المرسل: {form.cleaned_data['name']} - {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            return redirect('country_contact', country_slug=country.slug)
    return render(request, 'articles/country_contact.html', {
        'country': country,
        'form': form
    })

def country_privacy_policy_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    return render(request, 'articles/country_privacy_policy.html', {'country': country})

def country_terms_view(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    return render(request, 'articles/country_terms.html', {'country': country})

# ===============================================
# إنشاء sitemap لكل دولة
# ===============================================
def country_sitemap(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    categories = Category.objects.filter(country=country)
    articles = Article.objects.filter(country=country)

    xml_content = render_to_string("sitemaps/country_sitemap.xml", {
        "country": country,
        "categories": categories,
        "articles": articles,
        "request": request
    })

    return HttpResponse(xml_content, content_type="application/xml")

# إنشاء ملف robots.txt تلقائيًا


# توليد sitemap index لجميع الدول
def all_countries_sitemaps(request):
    countries = Country.objects.all()
    sitemap_links = [
        f"{request.scheme}://{request.get_host()}/sitemap/{country.slug}.xml"
        for country in countries
    ]
    content = render_to_string("sitemaps/all_countries_sitemap.xml", {
        "sitemap_links": sitemap_links
    })
    return HttpResponse(content, content_type="application/xml")