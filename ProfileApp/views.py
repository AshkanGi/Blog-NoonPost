from django.views import View
from .forms import UpdateEmailForm, UpdatePhoneForm
from django.contrib import messages
from django.shortcuts import render, redirect


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
        if full_name:
            user = request.user
            user.full_name = full_name
            user.save()
        return redirect('ProfileApp:edit')


class UpdatePhone(View):
    def post(self, request):
        form = UpdatePhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            user = request.user
            user.phone = phone
            user.save()
        return redirect('ProfileApp:edit')


class UpdateEmail(View):
    def post(self, request):
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = request.user
            user.email = email
            user.save()
        return redirect('ProfileApp:edit')



