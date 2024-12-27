import re
from django import forms
from AccountApp.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "password", "is_active", "is_admin"]


attrs = {
    'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left placeholder-transparent focus:outline-none focus:ring-0'
}


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs=attrs))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        phone = r'^\d{11}$'
        if re.match(email, username) or re.match(phone, username):
            return username
        else:
            raise forms.ValidationError('ورودی معتبر نیست. لطفا یک ایمیل معتبر یا شماره تلفن 11 رقمی وارد کنید')


class OTPVerifyForm(forms.Form):
    code = forms.CharField(max_length=5, widget=forms.TextInput(attrs=attrs))


class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs=attrs))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs=attrs))

    def clean(self):
        cd = super().clean()
        password = cd['password']
        confirm_password = cd['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('کلمه عبور مطابقت ندارد')
        return cd
