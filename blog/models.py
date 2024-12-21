from django.db import models
# برای ریدایرکت کردن یا تغییر مسیر فعلی به جایی ک میخواییم بره
from django.urls import reverse
from django.utils import timezone
from Extenshion.utils import jalali_converter
from django.utils.text import slugify
from django.utils.html import format_html
from account.models import User  # برای کلید خارجی مقالات در کلاس ارتیکل

from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from star_ratings.models import Rating


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(Status='p')
# my manager


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(statuses=True)


class IpAddress(models.Model):
    # _(""), protocol="both", unpack_ipv4=False ,
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')


class Category(models.Model):
    # تعریف بشه تا اگر یک زمانی والدی پاک شدبچه هاشم پاک بشن یا نon_delete برای کلید خارجی باید ارگومان
    # on_delete=models.SET_NULL پاک نشن بصورت دستی خواسیم پاک میکنیم
    # قراره هر دسته بندی والد خودش باشه ـــ بصورت پیشفرض دسته بندی ها والد نداشته باشن ـــ بتونه خالی باشه
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دسته')

    titles = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slugs = models.SlugField(max_length=100, unique=True,
                             verbose_name="آدرس دسته بندی", blank=True, null=True)
    # بولین... تیکشو بزنی ترو میشه نزنی فالس
    statuses = models.BooleanField(
        default=True, verbose_name="آیا نمایش داده شود؟")
    positions = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "عنوان دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        # آورد ینگ میاد روی کل مدل اعمال میشه اینجا... شبیه اگردرینگ مدل بعدیه
        # بوسیله پرنت لاین اندر لاین ایدی بصورت پیشفرض والد ها بالاتر از بچه ها قرار میگیرن
        ordering = ['parent__id', 'positions']
        # دلیل استفاده از پرنت اندر لاین اندر لاین ایدی بجای پرنت ... جلوگیری از ایجاد یک حلقه بینهایت از پرنته

    def __str__(self):
        return self.titles

    def save(self, *args, **kwargs):
        if not self.slugs:
            self.slugs = slugify(self.titles)
        super(Category, self).save(*args, **kwargs)

    objects = CategoryManager()  # تعیین منیجر برای کلاس مورد نظر


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیشنویس'),  # اگه درافت بود دی میزاره
        ('p', 'منتشر شده'),  # اگ پابلیش بود پی میزاره
        ('i', 'در حال بررسی'),  # میزاره i یا درحال بررسی کردن بود investigate اگر
        ('b', 'برگشت داده شده'),  # اگ بک بود بی میزاره
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='articles', verbose_name='نویسنده')
    Title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    # ادرس منحصر بفرده / اگه یونیک نباشه ارور میده
    Slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس مقاله')
    Category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name='articles')  # foreign key
    # تعیین نکردیم پس میتونه هر چیز و هر نوعی باشه فقط متن باشه
    Description = models.TextField(verbose_name='توضیحات')
    # برای استفاده از ایمیج ها در پایتون باید کتابخانه پیلو نصب باشه pillow
    # تعیین محل پوشه برای اپلود کردن عکس
    Thumbnail = models.ImageField(
        upload_to='images', verbose_name='تصویر مقاله')
    # زمانشو تعیین میکنه برا وقتی که ضفحه باز شد .. بصورت خود کار هروقت باز شد اون تاریخو نشون میده
    Publish = models.DateTimeField(
        default=timezone.now, verbose_name='زمان انتشار')
    # بصورت اتوماتیک مقالات یا هرچی مهم نیس کی و چجوری هروقت ایجاد شدن رو ذخیره کنه
    Created = models.DateTimeField(auto_now_add=True)
    # هروقت مقاله اپدیت شد رو ذخیره میکنه
    Updated = models.DateTimeField(auto_now=True)
    # انتخاب میکنه بین درافت و پابلیش .. وقتی انتخاب شد شرط اجرا میشه و بجا اونا دی یا پی قرار میگیره
    is_spacial = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    Status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    comments = GenericRelation(Comment)

    # برای ایجاد رابطه چند به چند بین کاربران یا همون ایپی ها با مقالات
    hits = models.ManyToManyField(
        IpAddress, through='ArticleHits', blank=True, related_name='hits', verbose_name='بازدیدها')

    ratings = GenericRelation(Rating)

    class Meta():
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-Publish']

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return jalali_converter(self.Publish)
    jpublish.short_description = 'زمان انتشار'

    # def category_published(self):
    #     # from category object in this models / وقتی ارتیکلی غیر فعال شد یا همون فالس شد قرار نیس نمایش داده بشه اونجا که با هشتگ هستن
    #     return self.Category.filter(statuses=True)

    def category_to_str(self):
        #  بجای اینکه از category.all استقاده کنیم از کتگوریـ پابلیشد استفاده میکنیم تا اگه ارتیکلی مثل اخبار رو نخواسیم و حذفش کردیم دیگ کلا از تو وبلاگ پاک بشه و نمایش داده نشه
        # از لیست مدل کتگوری استفاده بشه ن ارتیکل وگرنه ارور میده
        return "، ".join([categori.titles for categori in self.Category.active()])
    category_to_str.short_description = "دسته بندی "

    objects = ArticleManager()  # تعیین منیجر برای کلاس مورد نظر

    def Thumbnail_tag(self):  # تابعی برای ایجاد تصویر بند انگشتیدر لیست مقالات
        return format_html("<img width=120 hight=90 style='border-radius:5px' src='{}' >".format(self.Thumbnail.url))
    Thumbnail_tag.short_description = 'تصویر'

# Create your models here.


class ArticleHits(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)


# class Slides(models.Model):
#     Title = models.CharField(max_length=200)
#     image = models.ImageField(
#         upload_to='images')
#     Publish = models.DateTimeField(
#         default=timezone.now)
#     Created = models.DateTimeField(auto_now_add=True)
#     Updated = models.DateTimeField(auto_now=True)
#     statuses = models.BooleanField(
#         default=False)

#     class Meta():
#         ordering = ['-Publish']

#     def __str__(self):
#         return self.Title

# class SlideShow(models.Model):
#     slide = models.OneToOneField(Slides,on_delete=models.CASCADE)
#     statuses = models.BooleanField(
#         default=False)

#     class Meta():
#         ordering = ['-article__Publish']

#     def __str__(self):
#         return self.article.Title