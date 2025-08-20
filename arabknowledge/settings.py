"""
Django settings for arabknowledge project.
"""

from pathlib import Path

# ========================
# Paths
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Security
# ========================
SECRET_KEY = 'django-insecure-h(ky(ezdvyi463^9r)u5!@2z5!th-%4^ocd#fdj0yl@h%@9$!+'
DEBUG = False  # يجب إيقاف debug في الإنتاج
ALLOWED_HOSTS = ['*']  # ضع هنا الدومينات الفعلية

# ========================
# Custom User
# ========================
AUTH_USER_MODEL = 'articles.CustomUser'

# ========================
# Applications
# ========================
INSTALLED_APPS = [
    'jazzmin',  # لازم يكون أول تطبيق
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Whitenoise
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # تطبيقاتك
    'dashboard',
    'articles',
    'ckeditor',
    'ckeditor_uploader',
]

# ========================
# Jazzmin
# ========================
JAZZMIN_SETTINGS = {
    "site_title": "ArabPedia Admin",
    "site_header": "لوحة إدارة ArabPedia",
    "site_brand": "ArabPedia",
    "welcome_sign": "مرحباً بك في لوحة التحكم",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["articles", "auth"],
    "icons": {
        "articles": "fas fa-newspaper",
        "articles.article": "fas fa-file-alt",
        "articles.country": "fas fa-flag",
        "articles.category": "fas fa-tags",
        "auth.user": "fas fa-user",
    },
    "topmenu_links": [
        {"name": "الصفحة الرئيسية", "url": "/", "new_window": False},
        {"model": "auth.user"},
    ],
    "language_chooser": True,
}

# ========================
# Email
# ========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@tariqaljoda.com'
EMAIL_HOST_PASSWORD = 'Yaser2008@'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ========================
# Auth
# ========================
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'

# ========================
# Middleware
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise لخدمة static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arabknowledge.urls'

# ========================
# Templates
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'arabknowledge.wsgi.application'

# ========================
# Database (Production - PostgreSQL Render)
# ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'arabknowledge_db',
        'USER': 'arabknowledge_db_user',
        'PASSWORD': 'GLMiIasX9aiSTVmcpB8uDU74uIcuAlh2',
        'HOST': 'dpg-d2ih7bbuibrs739qrelg-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

# ========================
# Password Validation
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# Static files (Production)
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"  # تجمع كل ملفات static هنا عند collectstatic
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ========================
# Media files
# ========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ========================
# Default primary key field type
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================
# CKEditor
# ========================
CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'language': 'ar',
    },
}
