# for using listview , DetailView
# from .forms import SignUpForm , UserLoginForm
from django.views.generic import ListView, DetailView

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import activate

from account.models import User
from account.mixins import AuthorAccessMixin

from .models import Article, Category

from django.db.models import Q
# from django.db.models import Count , Q
# from datetime import datetime , timedelta
# def home(request , page=1):
#      # چون تو خود مدل اوردرینگ دادیم که پوزیشن بود اینجا نیازی بهش نیس
#     contact_list = Article.objects.published()#  اون مواردی که استتوسشون برابر با پابلیش بود و بصورت نزولی نمایش داده میشن
#     paginator = Paginator(contact_list, 6)# تعریف تعداد مورد (مقاله) در هر صفحه / مقاله هارم از کانتکت لیست میگیره
#     page_number = request.GET.get(page)
#     ''' تعریف شده و باید همین کلمه باشه تا کار کنه یا از هردو طرف تغییر پیدا کنه home.html لازم به ذکره که این کلمه در فایل  page درخواست فرستادن برای گرفتن شماره '''
#     contacts = paginator.get_page(page) # دریافت شماره صفحه و ریختنش در یک متغیر
#     data = {

#         'articles':contacts,
#     }
#     return render(request , 'blog/home.html' , data)


# بالایی بنابر این هرجا اسم تابع بالایی بود رو حذف و بجاس اسم این کلاس رو میزاریم home به جای تابع
class Article_list(ListView):
    # model = article  # میاد بدون هیچ قانون و شرایط خاصی هرچی مقاله بود رو نشون میده ک نمیخواییم
    # template_name = 'blog/home.html'  # تعیین مسیر قالب ... ولی خود جنگو طبق یسری قانون خودش مسیرو میگیره
    # context_object_name = 'articles'   # نیازی به اینم نداریم چون جنگو خودش میاد ی نامی که استفاده شده رو میگیره و قرار میده خودش = این نام برای گرفتن مقالات استفاده شده
    # اون مواردی که استتوسشون برابر با پابلیش بود و بصورت نزولی نمایش داده میشن
    model = Article
    queryset = Article.objects.published()
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # دریافت شیء پیجیناتور بر اساس مقادیر queryset و paginate_by
        paginator = Paginator(self.queryset, self.paginate_by)

        # دریافت شماره صفحه از پارامتر صفحه درخواستی برای برگرداندن
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        # اضافه کردن اطلاعات مربوط به آخرین صفحه به context
        context['last_page'] = page_obj

        return context 
    


# Q(articlehits__created__year = 2020) # مقالاتی ک در سال ۲۰۲۰ هستنو نشون میده
# Q(articlehits__created__month = 10) # مقالاتی که در ماه ۱۰ همه سالها هستن رو نشون میده
# Q(articlehits__created__year = 2020) | Q(articlehits__created__month = 10) # |or &and  ترکیبی از هردو مورد بالا ...


# def detail_article(request , slug):
#     # try:  يه جنگو کار نباس این کارو بکنه کد نوشتن زیادی و هارد کدینگه
#     #     article= Article.objects.get(Slug=slug)# از دیتابیس ارتیکل میره بخش اسلاگ ها و اون اطلاعاتو میریزه تو متغییر اسلاگ
#     # except Exception as e:
#     #     raise Http404
#     data = {
#         'article': get_object_or_404(Article , Slug=slug , Status = 'p')
    # }
    # return render(request , 'blog/detail.html' , data)


class Detail_list(DetailView):

    def get_object(self):
        # میاد هرچی ک مال اسلاگه رو میگیره = هرمقداری اسلاگ داشت رو میگیره   تعریف اسلاگ
        slug = self.kwargs.get('slug')
        # اینجا تعیین کردیم که از مدل .. اسلاگ برابر با اسلاگه
        article = get_object_or_404(Article, Slug=slug, Status='p')
        
        ip_address = self.request.META['ip_address']
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        
        return article


# def category(request , slug , page=1):
#     category = get_object_or_404(Category , slugs=slug , statuses =True)# برای دسته بندی های سایت که مثلا تو دسته بندی اخبار چه مقاله هایی وجود داره اونارو نمایش میده
#     category_list = category.articles.published()
#     paginator = Paginator(category_list, 6)# تعریف تعداد مورد (مقاله) در هر صفحه / مقاله هارم از کانتکت لیست میگیره
#     page_number = paginator.get_page(page)
#     """
#      در اینجا روند پاسکاری و میشه در نهایت میرسه به این .. اول مقالات در ارتیکل لیست گرفته
#       و داده میشه پیجینیتور که در هر صفحه ۶ مقاله رو تنظیم میکنه
#       بعد تنظیم شدن صفحه بندی میرسه به این تا بالاخره صفحاتو نشون بده(اگ این مشکل داشته باشه هیچی نشون داده نمیشه)
#     """
#     data = {
#         'category' : category , # اینجا میاییم از فایل مودل کلاس کتگوری رو ازش مخواییم مخواییم طبق تعریفی که به متغییر کردیم
#         'articles' : page_number # اینو بگیری انگار متغیرای بالاترشو گرفتی
#     }
#     return render(request , 'blog/category.html' , data)
class Category_list(ListView):

    paginate_by = 5
    template_name = 'blog/category_list.html'  # مسیر دهی برای اجرای فایل مورد نظر

    def get_queryset(self):
        global category
        # میاد هرچی ک مال اسلاگه رو میگیره = هرمقداری اسلاگ داشت رو میگیره   تعریف اسلاگ
        slug = self.kwargs.get('slug')
        # استفاده از منیجر
        # اینجا تعیین کردیم که از مدل .. اسلاگس برابر با اسلاگه
        category = get_object_or_404(Category.objects.active(), slugs=slug)
        return category.articles.published()  # ارسال لیست مقالات
        # return super().get_queryset()

    def get_context_data(self, **kwargs):  # تابع درونی جنگو برای متنها(کانتکست ها )
        context = super().get_context_data(**kwargs)
        context["category"] = category
        return context




class Author_list(ListView):


    paginate_by = 5
    template_name = 'blog/author_list.html'  # مسیر دهی برای اجرای فایل مورد نظر

    def get_queryset(self):
        global author
        # میاد هرچی ک مال اسلاگه رو میگیره = هرمقداری اسلاگ داشت رو میگیره   تعریف اسلاگ
        username = self.kwargs.get('username')
        # استفاده از منیجر
        # اینجا تعیین کردیم که از مدل .. اسلاگس برابر با اسلاگه
        author = get_object_or_404(User, username=username)
        return author.articles.published()  # ارسال لیست مقالات
        # articles from related_name of author
        # return super().get_queryset()

    def get_context_data(self, **kwargs):  # تابع درونی جنگو برای متنها(کانتکست ها )
        context = super().get_context_data(**kwargs)
        context["author"] = author
        return context


class ArticlePreview(AuthorAccessMixin,DetailView):

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)




# search box

class Search_list(ListView):

    paginate_by = 5
    template_name = 'blog/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q') # q = query ک تعریفش کردیم ... ت سرچ

        return Article.objects.filter(Q(Description__icontains=search) | Q(Title__icontains=search) ) #  به بزرگی و کوچکی حروف حساسه contains / به بزرگی و کوچکی حروف حساس نیس  icontains 

    def get_context_data(self, **kwargs):  # تابع درونی جنگو برای متنها(کانتکست ها )
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get('q')
        return context



def change_lang(request):
    activate(request.GET.get('lang'))# get دریافت زبان از طریق متد 
    return redirect(request.GET.get('next'))


# def login_view(request):
#     if request.method == 'POST':
#         # پردازش داده های یک فرم لاگین درخواست شده
#         username = request.POST['username']
#         password = request.POST['password']

#         # تأیید هویت کاربر
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # ورود کاربر به سیستم
#             login(request, user)
#             return redirect('home')
#         else:
#             # گزینه ای مناسب برای خطای احراز هویت
#             errors['auth'] = "Username and/or password incorrect"
#             return render(request, 'accounts/login.html', {'errors': errors})
#     else:
#         return render(request, 'accounts/login.html')


# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             # ذخیره همه داده ها
#             user = form.save()

#             # ورود  کاربر به سیستم بعد از ساخت حساب
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect('home')


# Create your views here.
