from random import randint
from AccountApp.models import OTP
from django.core.mail import send_mail


def send_otp(username):
    code = randint(10000, 99999)
    print(code)
    OTP.objects.filter(username=username).delete()
    OTP.objects.create(username=username, code=code)
    if '@' in username:
        send_mail(
            'Welcome to NoonPost Shop',
            f'Your OTP code is {code}',
            'AshkanGhodrati0@gmail.com',
            [username]
        )
    else:
        pass  # سامانه sms