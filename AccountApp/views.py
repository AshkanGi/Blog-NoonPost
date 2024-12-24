from .utils import send_otp
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from AccountApp.models import User, OTP
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, OTPVerifyForm, LoginForm, ResetPasswordForm


class BaseView(View):
    template_name = None
    form = None

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            return self.form_valid(request, form)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, request, form):
        pass


class RegisterView(BaseView):
    template_name = 'AccountApp/Register-Login.html'
    form = RegisterForm

    def form_valid(self, request, form):
        username = form.cleaned_data.get('username')
        request.session['username_info'] = {'username': username}
        if User.objects.filter(username=username).exists():
            return redirect('AccountApp:login')
        send_otp(username)
        messages.success(request, "کد تأیید ارسال شد.")
        return redirect('AccountApp:verify_code')


class VerifyCodeView(BaseView):
    template_name = 'AccountApp/Verify-Otp.html'
    form = OTPVerifyForm

    def form_valid(self, request, form):
        username = request.session.get('username_info', {}).get('username')
        if not username:
            messages.error(request, "مشکلی در ارتباط با سرور به وجود آمد. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:register')
        otp_instance = OTP.objects.get(username=username)
        if not otp_instance or otp_instance.is_expired():
            messages.error(request, "کد تایید منقضی شده یا نامعتبر است, لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:register')
        if form.cleaned_data.get('code') == otp_instance.code:
            user = User.objects.create(username=username)
            login(request, user)
            otp_instance.delete()
            request.session.pop('username_info', None)
            return redirect('HomeApp:Home')
        form.add_error('code', 'کد معتبر نمیباشد.')
        return render(request, self.template_name, {'form': form})


class LoginView(BaseView):
    template_name = 'AccountApp/Login-Password.html'
    form = LoginForm

    def form_valid(self, request, form):
        username = request.session.get('username_info', {}).get('username')
        if not username:
            messages.error(request, "مشکلی در ارتباط با سرور به وجود آمد. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:register')
        user = authenticate(username=username, password=form.cleaned_data.get('password'))
        if user:
            login(request, user)
            request.session.pop('username_info', None)
            return redirect('HomeApp:Home')
        form.add_error('password', 'رمز عبور معتبر نمیباشد.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('HomeApp:Home')


class ForgetView(BaseView):
    template_name = 'AccountApp/Forget.html'
    form = RegisterForm

    def form_valid(self, request, form):
        username = form.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            request.session['username_info'] = {'username': username}
            send_otp(username)
            messages.success(request, "کد تأیید ارسال شد.")
            return redirect('AccountApp:forget_otp')
        form.add_error('username', 'شماره موبایل یا ایمیل وارد شده وجود ندارد.')
        return render(request, self.template_name, {'form': form})


class ForgetOTPVerifyView(BaseView):
    template_name = 'AccountApp/Verify-Otp.html'
    form = OTPVerifyForm

    def form_valid(self, request, form):
        username = request.session.get('username_info', {}).get('username')
        if not username:
            messages.error(request, "مشکلی در ارتباط با سرور به وجود آمد. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:forget')
        otp_instance = OTP.objects.get(username=username)
        if not otp_instance or otp_instance.is_expired():
            messages.error(request, "کد تایید منقضی شده یا نامعتبر است, لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:forget')
        if form.cleaned_data['code'] == otp_instance.code:
            otp_instance.delete()
            return redirect('AccountApp:reset_password')
        form.add_error('code', 'کد معتبر نمیباشد.')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(BaseView):
    template_name = 'AccountApp/Forget-Reset.html'
    form = ResetPasswordForm

    def form_valid(self, request, form):
        username = request.session.get('username_info', {}).get('username')
        user = User.objects.get(username=username)
        if not user:
            messages.error(request, "مشکلی در دریافت اطلاعات به وجود آمده. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:forget')
        password = form.cleaned_data.get('password')
        if password == form.cleaned_data.get('confirm_password'):
            user.password = make_password(password)
            user.save()
            request.session.pop('username_info', None)
            return redirect('AccountApp:register')
        form.add_error('confirm_password', 'رمزها با یکدیگر مطابقت ندارند.')
        return render(request, self.template_name, {'form': form})


class EnterOTPView(BaseView):
    template_name = 'AccountApp/Forget.html'
    form = RegisterForm

    def form_valid(self, request, form):
        username = form.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            request.session['username_info'] = {'username': username}
            send_otp(username)
            messages.success(request, "کد تأیید ارسال شد.")
            return redirect('AccountApp:enter_otp_verify')
        form.add_error('username', 'شماره موبایل یا ایمیل وارد شده وجود ندارد.')
        return render(request, self.template_name, {'form': form})


class EnterOTPVerifyView(BaseView):
    template_name = 'AccountApp/Verify-Otp.html'
    form = OTPVerifyForm

    def form_valid(self, request, form):
        username = request.session.get('username_info', {}).get('username')
        if not username:
            messages.error(request, "مشکلی در دریافت اطلاعات به وجود آمده. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:register')
        user = User.objects.get(username=username)
        if not user:
            messages.error(request, "مشکلی در دریافت اطلاعات به وجود آمده. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:register')
        otp_instance = OTP.objects.get(username=user)
        if not otp_instance or otp_instance.is_expired():
            messages.error(request, "کد تایید منقضی شده یا نامعتبر است, لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:enter_otp')
        if form.cleaned_data.get('code') == otp_instance.code:
            login(request, user)
            otp_instance.delete()
            request.session.pop('username_info', None)
            return redirect('HomeApp:Home')
        form.add_error('code', 'کد معتبر نمیباشد.')
        return render(request, self.template_name, {'form': form})


class ResendOTPView(View):
    def post(self, request):
        username = request.session.get('username_info', {}).get('username')
        if not username:
            messages.error(request, "مشکلی در دریافت اطلاعات به وجود آمده. لطفا مجدد تلاش کنید.")
            return redirect('AccountApp:forget')
        send_otp(username)
        return JsonResponse({"success": True, "message": "کد جدید ارسال شد."})