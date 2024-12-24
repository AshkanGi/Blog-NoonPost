import re
from django import forms


class UpdateEmailForm(forms.Form):
    email = forms.EmailField(max_length=225, widget=forms.TextInput(attrs={'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left placeholder-transparent focus:outline-none focus:ring-0'}))


class UpdatePhoneForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-left placeholder-transparent focus:outline-none focus:ring-0'}))

    def clean_username(self):
        username = self.cleaned_data.get('phone')
        phone = r'^\d{11}$'
        if re.match(phone, username):
            return username
        else:
            raise forms.ValidationError('ورودی معتبر نیست. لطفا یک شماره تلفن 11 رقمی وارد کنید')


