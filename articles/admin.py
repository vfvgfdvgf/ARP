from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Country, Category, Article, Employee

# ========================
# إدارة المستخدمين المخصصين
# ========================
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('صلاحية المستخدم', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('صلاحية المستخدم', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# ========================
# Inline للتصنيفات
# ========================
class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ('name', 'slug', 'description', 'image', 'image_url', 'preview_image')
    readonly_fields = ('preview_image',)

    def save_model(self, request, obj, form, change):
        if not obj.country_id:
            obj.country = self.parent_object
        obj.save()

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_object = obj
        return super().get_formset(request, obj, **kwargs)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="60"/>', obj.image_url)
        return "-"
    preview_image.short_description = "معاينة الصورة"

# ========================
# Inline للمقالات
# ========================
class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1
    fields = ('title', 'slug', 'category', 'author', 'image', 'image_url', 'preview_image')
    readonly_fields = ('preview_image',)

    def save_model(self, request, obj, form, change):
        if not obj.country_id:
            obj.country = self.parent_object
        obj.save()

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_object = obj
        return super().get_formset(request, obj, **kwargs)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="60"/>', obj.image_url)
        return "-"
    preview_image.short_description = "معاينة الصورة"

# ========================
# Inline للموظفين
# ========================
class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1
    fields = ('user', 'position', 'joined_at')
    readonly_fields = ('joined_at',)

# ========================
# إدارة الدول مع التصنيفات والمقالات والموظفين
# ========================
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview_image')
    fields = ('name', 'slug', 'image', 'image_url', 'preview_image')
    readonly_fields = ('preview_image',)
    inlines = [CategoryInline, ArticleInline, EmployeeInline]  # تم إضافة EmployeeInline

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100"/>', obj.image_url)
        return "-"
    preview_image.short_description = "معاينة الصورة"

# ========================
# إدارة التصنيفات (مستقلة)
# ========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'preview_image')
    fields = ('name', 'slug', 'country', 'description', 'image', 'image_url', 'preview_image')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100"/>', obj.image_url)
        return "-"
    preview_image.short_description = "معاينة الصورة"

# ========================
# إدارة المقالات (مستقلة)
# ========================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'category', 'author', 'created_at', 'preview_image')
    fields = ('title', 'slug', 'content', 'image', 'image_url', 'country', 'category', 'author', 'preview_image')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100"/>', obj.image_url)
        return "-"
    preview_image.short_description = "معاينة الصورة"

# ========================
# إدارة الموظفين (مستقلة)
# ========================
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'position', 'joined_at')
    list_filter = ('country',)
    search_fields = ('user__username', 'position')
