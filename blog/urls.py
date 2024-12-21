from django.urls import path 
from .views import (
    Detail_list ,
    Category_list , 
    Article_list  , 
    Author_list , 
    ArticlePreview,
    Search_list,
    )

# , login_view , signup_view , logout_view



app_name = 'blog' # تعیین اسم از هاردکدینگ در کد جلو گیری میکنه
urlpatterns = [
    # استفاده کنیم جلوی نام کلاس .as_view()  برای استفاده از کلاس باید
    path('' , Article_list.as_view(), name = 'home'),# تعیین ادرس برای صفحه اصلی – رشته باید خالی باشه
    path('page/<int:page>' , Article_list.as_view() , name = 'home'),
    path('article/<slug:slug>' , Detail_list.as_view() , name = 'detail_article') ,# ایجاد صفحه دوم
    path('category/<slug:slug>' , Category_list.as_view() , name = 'category') ,
    path('category/<slug:slug>/page/<int:page>' , Category_list.as_view() , name = 'category') ,
    
    path('author/<slug:username>' , Author_list.as_view() , name = 'author') ,
    path('author/<slug:username>/page/<int:page>' , Author_list.as_view() , name = 'author') ,
    path('preview/<int:pk>' , ArticlePreview.as_view() , name = 'preview') ,

    path('search/>' , Search_list.as_view() , name = 'search') ,
    path('search/page/<int:page>' , Search_list.as_view() , name = 'search') ,

    # path('signup/', signup_view, name='signup'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
]
