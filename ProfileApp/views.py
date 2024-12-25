from django.views import View
from AccountApp.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import UpdateEmailForm, UpdatePhoneForm


class ProfileDashboard(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-dashboard.html')


class ProfileFavorites(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-favorite.html')


class ProfileRecent(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-recent.html')


class ProfileEdit(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-edit.html')


class UpdateFullName(View):
    def post(self, request):
        full_name = request.POST.get('full_name')
        if full_name and len(full_name) <= 50:
            user = request.user
            user.full_name = full_name
            user.save()
            messages.success(request, 'نام کامل با موفقیت به‌روزرسانی شد.')
        else:
            messages.error(request, 'فیلد نمی‌تواند خالی باشد یا بیشتر از 50 کلمه باشد.')
        return redirect('ProfileApp:edit')


class UpdatePhone(View):
    def post(self, request):
        form = UpdatePhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            if User.objects.filter(phone=phone).exists():
                messages.error(request, 'این شماره تلفن قبلاً استفاده شده است.')
            else:
                user = request.user
                user.phone = phone
                user.save()
                messages.success(request, 'شماره تلفن با موفقیت به‌روزرسانی شد.')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نیست.')
        return redirect('ProfileApp:edit')


class UpdateEmail(View):
    def post(self, request):
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'این ایمیل قبلاً استفاده شده است.')
            else:
                user = request.user
                user.email = email
                user.save()
                messages.success(request, 'ایمیل با موفقیت به‌روزرسانی شد.')
        else:
            messages.error(request, 'ایمیل وارد شده معتبر نمیباشد.')
        return redirect('ProfileApp:edit')


class ChangePassword(View):
    def post(self, request):
        user = request.user
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if check_password(password, user.password):
            if new_password and confirm_password:
                if len(new_password) < 8:
                    messages.error(request, 'رمز عبور جدید باید حداقل ۸ کاراکتر باشد.')
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
                    return redirect('ProfileApp:edit')
                else:
                    messages.error(request, 'رمز عبور جدید و تأیید آن مطابقت ندارند.')
            else:
                messages.error(request, 'فیلدهای رمز عبور نباید خالی باشند.')
        else:
            messages.error(request, 'رمز عبور فعلی اشتباه است.')
        return redirect('ProfileApp:edit')
