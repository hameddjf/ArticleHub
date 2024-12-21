from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserForms(forms.ModelForm):
    def __init__(self , *args, **kwargs):
        user = kwargs.pop('user')#یوزری ک در دیکشنری وی کلاس پروفایل تعریف کردیم رو حذف میکنه

        super(UserForms , self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None # پاک کردن یا اضافه کردن یک متن راهنما برای فیلد مورد نظر که مشخص کردیم
 
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['spacial_user'].disabled = True
            self.fields['is_author'].disabled = True
        
    class Meta:
        model = User # باشه وگرنه ارور میده model لازمه نام متغیر
        # ModelForm has no model class specified.
        fields = ['username' , 'email' , 'first_name' , 'last_name' , 'spacial_user' , 'is_author']
        

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')