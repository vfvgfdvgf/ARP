from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField  # محرر CKEditor يدعم الصور والفيديو

# ========================
# موديل الدول
# ========================
class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='countries/', blank=True, null=True, verbose_name="صورة الدولة")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط صورة الدولة")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========================
# موديل التصنيفات
# ========================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(blank=True, null=True, verbose_name="وصف التصنيف")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="صورة التصنيف")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط صورة التصنيف")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========================
# موديل المقالات
# ========================
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextUploadingField(verbose_name="محتوى المقال")  # محرر CKEditor
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # الصور
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط صورة المقال")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="صورة المقال")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_main_image(self):
        """إرجاع الصورة سواء من الرابط أو المرفوع"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None

    def __str__(self):
        return self.title

# ========================
# موديل المستخدم المخصص
# ========================
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_admin(self):
        return self.role == 'admin'

    def is_editor(self):
        return self.role in ['admin', 'editor']

from django.db import models
from django.utils import timezone

class Comment(models.Model):
    article = models.ForeignKey('Article', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.article.title}"




# ========================
# موديل الموظف لكل دولة
# ========================
class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="الوظيفة")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.country.name})"
