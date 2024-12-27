from . import views
from django.urls import path

app_name = 'AccountApp'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify_code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forget/', views.ForgetView.as_view(), name='forget'),
    path('forget_otp/', views.ForgetOTPVerifyView.as_view(), name='forget_otp'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('enter_otp/', views.EnterOTPView.as_view(), name='enter_otp'),
    path('enter_otp_verify/', views.EnterOTPVerifyView.as_view(), name='enter_otp_verify'),
    path('resend_otp/', views.ResendOTPView.as_view(), name='resend_otp'),
]
