from django import forms
from user_app.models import UserInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserInfoForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields = ('profile_url','profile_pic')