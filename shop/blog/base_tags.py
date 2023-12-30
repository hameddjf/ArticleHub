from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe


register = template.Library()


# ایجاد یک تگ برای نمایش منوی ورود و خروج کاربر
@register.simple_tag(takes_context=True)
def auth_links(context):
    request = context['request']

    # بررسی اینکه کاربر وارد شده یا خروج کرده است
    if request.user.is_authenticated:
        logout_url = reverse('logout')
        link_str = f'<a class="nav-link" href="{logout_url}">خروج</a>'
    else:
        login_url = reverse('login')
        signup_url = reverse('signup')
        link_str = f'<a class="nav-link" href="{login_url}">ورود</a> | <a class="nav-link" href="{signup_url}">ثبت نام</a>'

    return mark_safe(link_str)
