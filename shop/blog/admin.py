from django.contrib import admin
from .models import Article,   Category , IpAddress  # فراخوانی کلاس مدل در پنل ادمین
from django.contrib import messages
from django.utils.translation import ngettext

from modeltranslation.admin import TranslationAdmin
# admin header change
admin.site.site_header = 'وبلاگ'

# غیر فعال کردن اکشن مورد نظر داخل استرینگ == فقط برای اکشن دیلیت کردن کار میکنه
# admin.site.disable_action("delete_selected")


@admin.action(description="انتشار مقالات انتحاب شده")
# ایجاد اکشن برای مقالاتی که پیشنویسن به منتشر شده
def make_published(self, request, queryset, ):

    updated = queryset.update(Status="p")  # Status from class Article of model
    self.message_user(
        request,
        ngettext
        (
            "%d مقاله با موفقیت به عنوان منتشر شده علامت گذاری شد.",
            "%d مقاله با موفقیت به عنوان منتشر شده علامت گذاری شذند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


@admin.action(description="پیشنویس مقالات انتحاب شده")
# ایجاد اکشن برای مقالاتی که منتشر شدن به پیشنویس
def make_draft(self, request, queryset):
    updated = queryset.update(Status="d")  # Status from class Article of model
    self.message_user(
        request,
        ngettext
        (
            "%d مقاله با موفقیت به عنوان پیشنویس شده علامت گذاری شد.",
            "%d مقاله با موفقیت به عنوان پیشنویس شده علامت گذاری شذند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


@admin.action(description="فعال کردن")
# ایجاد اکشن برای مقالاتی که پیشنویسن به منتشر شده
# فعال کردن دسته بندی یا دسته بندی های انتخابی در پنل ادمین
def make_active(self, request, queryset, ):

    # statuses from class Category of model
    updated = queryset.update(statuses=True)
    self.message_user(
        request,
        ngettext
        (
            "%d مقاله با موفقیت فعال شد.",
            "%d مقالات با موفقیت فعال شذند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


@admin.action(description="غیر فعال کردن")
# ایجاد اکشن برای مقالاتی که پیشنویسن به منتشر شده
# غیر فعال کردن دسته بندی یا دسته بندی های انتخابی در پنل ادمین
def make_disactive(self, request, queryset, ):

    # statuses from class Category of model
    updated = queryset.update(statuses=False)
    self.message_user(
        request,
        ngettext
        (
            "%d مقاله با موفقیت غیر فعال شد.",
            "%d مقالات با موفقیت غیر فعال شذند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('positions', 'titles', 'slugs', 'parent', 'statuses')
    actions = [make_active, make_disactive]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in self.list_display:
            if not isinstance(item, str):
                print(f"Invalid item in list_display: {item}")
    list_filter = (['statuses'])  # filter in blog
    # Creating a search menu based on title , description
    search_fields = ('titles', 'slugs')
    # فیلد اسلاگ قراره با فیلد تایتل همزمان پر شن
    prepopulated_fields = {'slugs': ('titles',)}


admin.site.register(Category, CategoryAdmin)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('Title','Thumbnail_tag', 'Slug', 'author','jpublish','is_spacial' , 'Status', 'category_to_str')
    list_filter = ('Publish', 'Status', 'author')  # filter in blog / نمایش لیست وار در پنل مدیریت
    # Creating a search menu based on title , description
    search_fields = ('Title', 'Description')
    # فیلد اسلاگ قراره با فیلد تایتل همزمان پر شن
    prepopulated_fields = {'Slug': ('Title',)}

    
    # ترتیب نمایش بر مبنای .. اول استاتوس بصورت صعودی بعد پابلیش بصورت نزولیه بخاطر منها
    ordering = ['Status', '-Publish']

    actions = [make_published, make_draft]  # اضافه کردن اکشن مورد نظر

    group_fieldsets = True

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
from django.conf import settings
admin.site.media = settings.MEDIA_URL


# استفاده از مدل ارتیکل در پنل ادمین
# admin.site.register(Article)
admin.site.register(IpAddress)

# Register your models here.
