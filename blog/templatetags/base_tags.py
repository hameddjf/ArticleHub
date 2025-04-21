from ..models import Category
from django import template

from ..models import Article, Category
from datetime import datetime , timedelta

from django.contrib.contenttypes.models import ContentType
from django.db.models import FloatField
from django.db.models import Count , Q
from django.utils.translation import gettext as _


register = template.Library()

@register.simple_tag
def title():
    return "وبلاگ جنگویی"

@register.inclusion_tag("blog/partials/categury_navbar.html")
def categury_navbar():
    return {"category":Category.objects.filter(statuses=True),} # چون تو خود مدل اوردرینگ دادیم که پوزیشن بود اینجا نیازی بهش نیس

@register.inclusion_tag("blog/partials/sidebar.html")
def popular_article():
    last_month = datetime.today() - timedelta(days=30)
    return {"articles":Article.objects.published().annotate(count=Count(# بر اساس تیبل هیتس باشه count 
    #تا ن که ازش استفاده میکنیم تا نتایجو به فیلتر بده Q object ی کوئری هس که عملیات فیلتر رو انجام میده... و برای اجرای این کوئری از ی ابجکتی به نام articlehits__created = last_month 
        'hits' , filter=Q(articlehits__Created__gt = last_month))).order_by( # وقتی دوتا اندرلاین گزاشتیم اصطلاحا لوک اپه ... یعنی از ی تیبل بتونیم از تیبلای دیگه استفاده کنیم  lookup
            '-count' , 'Publish')[:2], # اطلاعات بر اساس کانت مرتب کن .. مقاله با بازدید بیشتر بالاتر... یا مقاله جدیدتر بالاتر.. حداکثر ۵ تا مقالرو نمایش بده
            'Title':_("Most Viewed Articles of the Month")
        }

@register.inclusion_tag("blog/partials/sidebar.html")
def Hot_article():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='blog' , model='article').id #اپلیکیشن بلاگ ... مدل ارتیکل ... ایدیشو میخاییم اخرش دات ایدی میزاریم
    return {"articles":Article.objects.published().annotate(count=Count(
        #  اپ کامنت..فیلد پوستد که داره مربوط به تاریخ کامنت گزاشتن و کانتنت تایپ که مربوط ب ایدی مدلمون هستش که ایدی مدل ارتیکلمون برابر ۷ هستش ولی متغیری تعریف میکنیم برای گرفتن ایدیش که بهتره
        'comments' , filter=Q(comments__posted__gt = last_month) and Q(comments__content_type_id = content_type_id))).order_by( 
            '-count' , 'Publish')[:3],
            'Title':_("Most discussed articles of the month")
        }

@register.inclusion_tag("blog/partials/sidebar.html")
def Rating_article():
    
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    
    articles = Article.objects.published().annotate(count=Count(
        'ratings', filter=(Q(ratings__average__gt=content_type_id)&Q(ratings__count__gt=content_type_id))
    )).order_by('-ratings__count', '-ratings__average' , '-Publish')[:3]
    
    return {
        "articles": articles,
        "Title": _("high score articles")
    }

# @register.inclusion_tag("blog/partials/slide.html")
# def Slide():
#     return {
#         "category":Category.objects.filter(statuses=True , articles__tatus=True),
#     }



@register.inclusion_tag('registration/partials/link.html')
def link(request , link_name , content , classes):
    return {
        'request' : request ,
        'link_name' : link_name , # name of addres
        'link' : 'account:{}'.format(link_name) , # addres
        'content' : content,
        'classes' : classes,
    }