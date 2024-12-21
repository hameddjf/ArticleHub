from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required# قابلیتی از جنگو برای ضروری کردن ورود کردن به ضفحه سایت
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , PasswordChangeView
from django.views.generic import ListView , CreateView , UpdateView , DeleteView 
from blog.models import Article
from .models import User
from .forms import UserForms , SignupForm
from .mixins import (
    FieldsMixin , 
    FormMixin , 
    AuthorAccessMixin , 
    SuperUserAccessMixin ,
    AuthorsAccessMixin, )
from django.urls import reverse_lazy
from .tokens import account_activation_token
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.mail import EmailMessage



# Create your views here.

# @login_required
# def home(request): # در این صفحه ضروریه که کاربر ورود کرده کرده باشه غیر این براش نمیاد این صفحه
#     return render(request , 'registration/home.html')

class Article_list(AuthorsAccessMixin , ListView): # بنظر بلطف میکسین طرف با ی بار ورود جلسش ذخیره میشه و با ی بار رفرش پاک نمیشه / هرچند لزوم دیدن این صفحه به ورود کردن ضروریه
    template_name = 'registration/home.html'

    def get_queryset(self): # نحوه دادن دسرسی کاربر به مقالات
        if self.request.user.is_superuser:#  اگر کاربر سوپر یوزر بود همه مقالاتو بتونه ببینه
            return Article.objects.all()
        else:# در غیر اینصورت اگر یک کاربر عادی بود فقط بتونه مقالات خودشو ببینه
            return Article.objects.filter(author=self.request.user)


class Article_Create(AuthorsAccessMixin , FormMixin , FieldsMixin , CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'

class Article_Update(AuthorsAccessMixin , FormMixin , FieldsMixin , UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class AuthorDelete(SuperUserAccessMixin , DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin,UpdateView):#LoginRequiredMixin باعث میشه کسی ک ورود نکرده نتونه ب پروفایل دسرسی داشته باشه
    model = User
    template_name = 'registration/profile.html'
    # fields = ['username' , 'email' , 'first_name' , 'last_name' , 'spacial_user' , 'is_author']
    form_class = UserForms
    success_url = reverse_lazy('account:profile') # تغییر مسیر بعد از زدن دکمه ویرایش اطلاعات ... دباره میره به همون صفحه پروفایل

    def get_object(self): # برای امنیت بیشتر که یوزر با تغییر دادن ایدی عددی نتونه وارد پروفایل شخص دیگ بشه

        return User.objects.get(pk = self.request.user.pk) 
        # همین یوزری ک لاگین کرده پرایمری کی اونو بگیر و بعد از لیست یوزر ها ابجکتیو برگردون ک پرایمری کی اون همین یوزر فعلی باشه

    def get_form_kwargs(self):
        kwargs = super(Profile , self).get_form_kwargs() # باید اول پروفایل باشه بعد سلف وگرنه ارور میده
        kwargs.update({
            'user' : self.request.user

        })
        return kwargs

class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')# سوپر یوزر یا نویسنده مقالات نوشته شده بود میره ب لیست مقالات یا همون هوم پنل مدیریتی
        else:
            return reverse_lazy('account:profile')# غیر این ببره ب بخش پروفایل
        


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/authenticated.html')
    else:
        return redirect(reverse('failed'))


def authenticated_page(request):
    return render(request, 'registration/authenticated.html')

def confirmation_page(request):
    return render(request, 'registration/confirmation.html')
    
def failed_page(request):
    return render(request, 'registration/failed.html')

def authenticated_page(request):
    return render(request, 'registration/authenticated.html')

import re

class SignUp(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self , form ): # in the mixins
        user = form.save(commit=False)
        user.is_active = False

        # email = form.cleaned_data.get('email')
        # if not re.match(r"[^@]+@(gmail|yahoo)\.com$", email):
        #     # ایمیل ارائه شده اشتباه است
        #     return redirect("invalid/")

        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعالسازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain, # ادرس سایت
            'uid':urlsafe_base64_encode(force_bytes(user.pk)), # روشی برا ساخت یو ایدی
            'token':account_activation_token.make_token(user),# روشی برا ساخت توکن
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return redirect('confirmation/')
        # return redirect("registration/confirmation.html")

def email_invalid(request):
    return render(request, 'registration/email_invalid.html')

