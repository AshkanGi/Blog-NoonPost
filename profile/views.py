from slugify import slugify
from django.views import View
from account.models import User
from blog.models import Article, RecentVisit
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UpdateEmailForm, UpdatePhoneForm, ArticleForm, ChangePasswordForm
from django.contrib.auth.hashers import make_password


class ProfileDashboard(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-dashboard.html')


class ProfileFavorites(View):
    def get(self, request):
        liked_articles = Article.objects.filter(likes__user=request.user)
        return render(request, 'ProfileApp/profile-favorite.html', {'liked_articles': liked_articles})


class ProfileRecent(View):
    def get(self, request):
        recent_views = RecentVisit.objects.filter(user=request.user).order_by('-viewed_at')[:6]
        recent_articles = [view.article for view in recent_views]
        return render(request, 'ProfileApp/profile-recent.html', {'recent_articles': recent_articles})


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
            messages.error(request, 'ورودی معتبر نیست. لطفا یک شماره تلفن 11 رقمی وارد کنید.')
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
            messages.error(request, 'ورودی معتبر نیست. لطفا یک ایمیل معتبر وارد کنید')
        return redirect('ProfileApp:edit')


class ChangePassword(View):
    def post(self, request):
        user = request.user
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.password = make_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
            return redirect('ProfileApp:edit')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return redirect('ProfileApp:edit')


class UpdateImage(View):
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            messages.error(request, 'هیچ فایلی انتخاب نشده است.')
            return redirect('ProfileApp:edit')
        user = request.user
        user.image = image
        user.save()
        messages.success(request, 'تصویر با موفقیت آپلود شد.')
        return redirect('ProfileApp:edit')


class UpdateBio(View):
    def post(self, request):
        bio = request.POST.get('bio')
        if not bio:
            messages.error(request, 'فیلد راجب من خالی است.')
            return redirect('ProfileApp:edit')
        user = request.user
        user.bio = bio
        user.save()
        messages.success(request, 'توضیحات ثبت شد.')
        return redirect('ProfileApp:edit')


class ArticleCreateView(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'ProfileApp/profile-new-article.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            article = Article.objects.create(
                author=request.user,
                title=cd.get('title'),
                slug=slugify(cd.get('title'), allow_unicode=True),
                body=cd.get('body'),
                image=request.FILES.get('image'),
                status=cd.get('status', False),
            )
            article.category.set(cd.get('category', []))
            article.tags.set(cd.get('tags', []))
            return redirect('BlogApp:home')
        return render(request, 'ProfileApp/profile-new-article.html', {'form': form})