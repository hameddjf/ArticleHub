from django.http import Http404
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404 , redirect
from blog.models import Article

class FieldsMixin():
    def dispatch(self , request , *args ,  **kwargs):
        self.fields = ['author','Title','Slug','Category','Description','Thumbnail','Publish', 'is_spacial' , 'Status'] 
        if request.user.is_superuser :
            self.fields.append('author',)
        return super().dispatch(request , *args, **kwargs)

class FormMixin():
    def form_valid(self , form ):
        if self.request.user.is_superuser: # اگر کاربر فعلی سوپریوزر باشد، فرم بدون هیچگونه تغییری ذخیره می‌شود
            form.save()
        else:#اما اگر کاربر فعلی سوپریوزر نباشد، یک شی از فرم ذخیره می‌شود
            self.obj = form.save(commit = False) # commit = False ، یعنی هنوز به پایگاه داده ذخیره نشده است
            self.obj.author = self.request.user # شی با نام کاربر فعلی پر می‌شود author فیلد 
            if not self.obj.Status == 'i': # اگ یوزر وضعیتی جز ای تونس بفرسته بصورت اجباری وضعیت رو دی بزار
                self.obj.Status = 'd'
        return super().form_valid(form) # ذخیره میشه super فرم بوسیله 
        

class AuthorAccessMixin():#برای مجوز دسترسی کاربران به صفحات مخصوص ایجاد کنندگان مطالب (مثلا مقالات، پست ها، نظرات و ...) استفاده می‌شود. 
    def dispatch(self , request , pk , *args ,  **kwargs):# هس ک تو کلاس وظیفه انجام  پردازشارو داره api view یک dispatch تابع 
        # که کشخص کننده کلید عددی خاص هر مقالس بازیابی میشه pk با Article یک شی از کلاس  get_object_or_404 هنگامی که یک درخواست داخلی از این کلاس به سرور ارسال شود بوسیله تابع 
        article = get_object_or_404(Article , pk = pk)
        if Article.author == request.user and Article.Status in ['d' , 'b'] or request.user.is_superuser : # بررسی میشه ک کاربر سوپریوزره یا نویسنده مقاله(مالک مقاله) و مقاله پیشنویس باشه
            return super().dispatch(request , *args, **kwargs) # فرآیند را به پدر کلاس انتقال می‌دهد تا برای موارد دیگر در این کلاس استفاده شود و به صورت پیش فرض به اجرا درآید.
            # ارجا میده request , args , kwargs را از پدر کلاس فراخونی میکنه و به  dispatch متد 
          # پدر نیز به صورت خودکار فراخوانی می‌شوند و شما نیازی به فراخوانی آن‌ها ندارید dispatch متدهای super().dispatch با استفاده از ،
          # . بسیار مفید است. request، این روش برای اضافه کردن عملکرد به پدر کلاس، مانند تغییر فرایند پردازش 
        else:
            raise Http404('شما نمیتوانید این صفحه را مشاده کنید.')


class SuperUserAccessMixin():
    def dispatch(self , request , *args ,  **kwargs):
        if request.user.is_superuser :
            return super().dispatch(request , *args, **kwargs)
        else :
            raise Http404('شما نمیتوانید این صفحه را مشاده کنید.')


class AuthorsAccessMixin():# همه نویسنده هارو بررسی میکنهک همچین دسرسی دارن یا ن
    def dispatch(self , request , *args ,  **kwargs):# هس ک تو کلاس وظیفه انجام  پردازشارو داره api view یک dispatch تابع 
        if request.user.is_authenticated:
            if request.user.is_author or request.user.is_superuser : # بررسی میشه ک کاربر سوپریوزره یا نویسنده مقاله(مالک مقاله)
                return super().dispatch(request , *args, **kwargs) # فرآیند را به پدر کلاس انتقال می‌دهد تا برای موارد دیگر در این کلاس استفاده شود و به صورت پیش فرض به اجرا درآید.
            # ارجا میده request , args , kwargs را از پدر کلاس فراخونی میکنه و به  dispatch متد 
            # پدر نیز به صورت خودکار فراخوانی می‌شوند و شما نیازی به فراخوانی آن‌ها ندارید dispatch متدهای super().dispatch با استفاده از ،
            # . بسیار مفید است. request، این روش برای اضافه کردن عملکرد به پدر کلاس، مانند تغییر فرایند پردازش 
            else:
                return redirect('account:profile')#redirect = http_response + reverse_lazy

        else:
            return redirect('login')#redirect = http_response + reverse_lazy
