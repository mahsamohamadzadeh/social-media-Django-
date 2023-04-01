from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistratonForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        emailuser = self.cleaned_data['email']
        user = User.objects.filter(email=emailuser).exists()
        if user:
            raise ValidationError('this email already exists')
        return emailuser

    def clean_username(self):
        usernameuser = self.cleaned_data['username']
        user = User.objects.filter(username=usernameuser).exists()
        if user:
            raise ValidationError('this user alreadi exists')
        return usernameuser

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('password must match')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age', 'bio')
