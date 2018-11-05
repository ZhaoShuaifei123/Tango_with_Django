from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile


class UserForm(forms.ModelForm):
    #覆盖默认的password组件
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        #记得用元组，因为元组是有序的，而列表传递到浏览器是无序的
        fields=('username','password','email','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('website','picture')