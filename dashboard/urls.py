from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='dashboard_login'),
    path('logout/', LogoutView.as_view(), name='dashboard_logout'),
    path('', views.dashboard_view, name='dashboard_home'),
    path('country/<slug:country_slug>/', views.dashboard_country_view, name='dashboard_country'),
]
