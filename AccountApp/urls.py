from . import views
from django.urls import path

app_name = 'AccountApp'

url_patterns_data = [
    ('register', views.RegisterView),
    ('verify_code', views.VerifyCodeView),
    ('login', views.LoginView),
    ('logout', views.LogoutView),
    ('forget', views.ForgetView),
    ('forget_otp', views.ForgetOTPVerifyView),
    ('reset_password', views.ResetPasswordView),
    ('enter_otp', views.EnterOTPView),
    ('enter_otp_verify', views.EnterOTPVerifyView),
    ('resend_otp', views.ResendOTPView),
]

urlpatterns = [path(f'{pattern}', view.as_view(), name=pattern) for pattern, view in url_patterns_data]
