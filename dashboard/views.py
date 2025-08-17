from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.decorators import login_required
from articles.models import Country, Article, Category, Employee
from django.utils.decorators import method_decorator

# ===== تسجيل الدخول =====
class LoginView(DjangoLoginView):
    template_name = 'dashboard/login.html'

# ===== الصفحة الرئيسية للـ Dashboard =====
@login_required
def dashboard_view(request):
    countries_count = Country.objects.count()
    articles_count = Article.objects.count()
    categories_count = Category.objects.count()
    employees_count = Employee.objects.count()

    latest_articles = Article.objects.order_by('-created_at')[:5]

    context = {
        'countries_count': countries_count,
        'articles_count': articles_count,
        'categories_count': categories_count,
        'employees_count': employees_count,
        'latest_articles': latest_articles,
    }
    return render(request, 'dashboard/dashboard.html', context)

# ===== صفحة إدارة دولة محددة =====
@login_required
def dashboard_country_view(request, country_slug):
    country = Country.objects.get(slug=country_slug)
    articles = country.articles.all()
    categories = country.categories.all()
    employees = country.employees.all()

    return render(request, 'dashboard/dashboard_country.html', {
        'country': country,
        'articles': articles,
        'categories': categories,
        'employees': employees,
    })
