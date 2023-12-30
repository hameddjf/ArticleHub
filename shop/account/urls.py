from django.contrib.auth import views
from django.urls import path
from .views import (
    Article_list , 
    Article_Create , 
    Article_Update , 
    AuthorDelete ,
    Profile ,

)

app_name = 'account'
# urlpatterns = [
#     path("logout/", views.LogoutView.as_view(), name="logout"),
#     path(
#         "password_change/", PasswordChange.as_view()  , name="password_change"
#     ),
#     path(
#         "password_change/done/",
#         views.PasswordChangeDoneView.as_view(),
#         name="password_change_done",
#     ),
#     # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
#     # path(
#     #     "password_reset/done/",
#     #     views.PasswordResetDoneView.as_view(),
#     #     name="password_reset_done",
#     # ),
#     # path(
#     #     "reset/<uidb64>/<token>/",
#     #     views.PasswordResetConfirmView.as_view(),
#     #     name="password_reset_confirm",
#     # ),
#     # path(
#     #     "reset/done/",
#     #     views.PasswordResetCompleteView.as_view(),
#     #     name="password_reset_complete",
#     # ),
# ]

urlpatterns = [
    path('' , Article_list.as_view() , name = 'home'),# بنظر بلطف میکسین طرف با ی بار ورود جلسش ذخیره میشه و با ی بار رفرش پاک نمیشه / هرچند لزوم دیدن این صفحه به ورود کردن ضروریه
    path('article/create' , Article_Create.as_view() , name = 'article-create'), # تعیین مسیر برای اضافه کردن مقاله
    path('article/update/<int:pk>' , Article_Update.as_view() , name = 'article-update'),
    path('article/delete/<int:pk>' , AuthorDelete.as_view() , name = 'article-delete'),
    path('profile/' , Profile.as_view() , name = 'profile'),
]