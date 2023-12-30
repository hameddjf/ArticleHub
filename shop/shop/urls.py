"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings  # فراخوانی تنظیمات همین پروژه
from django.conf.urls.i18n import i18n_patterns
from account.views import Login, SignUp, activate, confirmation_page, failed_page, authenticated_page, email_invalid
from django.conf.urls.static import static
from django.conf import settings
from blog.views import change_lang

# from payment.views import go_to_gateway_view , callback_gateway_view
# from azbankgateways.urls import az_bank_gateways_urls

# admin.autodiscover()

urlpatterns = [

    path('ratings/', include('star_ratings.urls', namespace='ratings')),


    path('change_lang', change_lang, name='change_lang'),

    # path('bankgateways/', az_bank_gateways_urls()),
    # path('az_bank_gateways/' , go_to_gateway_view),
    # path('callback_gateway/' , callback_gateway_view),
]

urlpatterns += i18n_patterns(
    path('', include('blog.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('comment/', include('comment.urls')),
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),

    path('signup/confirmation/', confirmation_page, name='confirmation'),
    path('signup/failed/', failed_page, name='failed'),
    path('signup/invalid/', email_invalid, name='email_invalid'),
    path(
        'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),
    path('authenticated/', authenticated_page, name='authenticated'),

)

# urlpatterns += i18n_patterns (
#     *urlpatterns,
#     prefix_default_language=False,
# )

# تنظیماتی که برای پوشه عکسها و اینا کردیم رو تعریف میکنیم ک البته کاربردی جدیدا نداره
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
