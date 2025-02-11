import re
from django import forms
from django.contrib.auth.hashers import check_password

from blog.models import Article


class UpdatePhoneForm(forms.Form):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^\d{11}$'
        if re.match(pattern, phone):
            return phone
        else:
            raise forms.ValidationError('ورودی معتبر نیست. لطفا یک شماره تلفن 11 رقمی وارد کنید.')


class UpdateEmailForm(forms.Form):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return email
        else:
            raise forms.ValidationError('ورودی معتبر نیست. لطفا یک ایمیل معتبر وارد کنید')


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not check_password(current_password, self.user.password):
            raise forms.ValidationError('رمز عبور فعلی اشتباه است.')
        return current_password

    def clean(self):
        cd = super().clean()
        new_password = cd.get('new_password')
        confirm_password = cd.get('confirm_password')
        if new_password and len(new_password) < 8:
            self.add_error('new_password', 'رمز عبور جدید باید حداقل ۸ کاراکتر باشد.')
        if new_password != confirm_password:
            self.add_error('confirm_password', 'رمز عبور جدید و تأیید آن مطابقت ندارند.')
        return cd


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'category', 'tags', 'status']
