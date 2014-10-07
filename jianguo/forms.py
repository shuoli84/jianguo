# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError


class UploadProfileImage(forms.Form):
    """
    The form used to upload profile image for current user.
    """

    picture = forms.ImageField(max_length=300*1024)


class RegisterForm(forms.Form):
    email = forms.EmailField(label=u'邮箱')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    name = forms.CharField(label=u'姓名', max_length=32, min_length=1)
    invitation_code = forms.CharField(label=u'邀请码', max_length=64, required=False)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError(u'该邮箱已经注册')
        return value

    def save(self, request):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        name = self.cleaned_data['name']

        user = User()
        user.email = email
        user.username = email
        user.set_password(password)
        user.save()

        user.profile.name = name
        user.profile.save()
        return user


