from django.db import models
from AccountApp.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(unique=True, max_length=50, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(unique=True, max_length=50, allow_unicode=True, verbose_name='نامک')
    status = models.BooleanField(default=False, verbose_name='منتشر شود')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=50, verbose_name='عنوان برچسب')
    slug = models.SlugField(unique=True, max_length=50, allow_unicode=True, verbose_name='نامک')

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده مقاله')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='انتخاب دسته بندی')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags', verbose_name='انتخاب برچسب')
    title = models.CharField(unique=True, max_length=150, verbose_name='عنوان مقاله')
    slug = models.SlugField(unique=True, max_length=150, allow_unicode=True, verbose_name='نامک')
    image = models.ImageField(upload_to='articles', blank=True, null=True, verbose_name='بنر مقاله')
    body = RichTextUploadingField(verbose_name='محتوای مقاله')
    status = models.BooleanField(default=False, verbose_name='منتشر شود')
    view = models.IntegerField(default=0, editable=False, verbose_name='بازدید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def article_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="80px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')

    def get_absolute_url(self):
        return reverse('BlogApp:article_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Message(models.Model):
    fullname = models.CharField(max_length=30, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='آدرس ایمیل')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')

    class Meta:
        verbose_name = 'تماس'
        verbose_name_plural = 'تماس ها'

    def __str__(self):
        return f'{self.email} - {self.subject}'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    body = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    status = models.BooleanField(default=True, verbose_name='منتشر شود')

    def __str__(self):
        return f'{self.article} - {self.user}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name = 'آدرس ایمیل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'تاریخ عضویت')

    class Meta:
        verbose_name = 'عضو خبرنامه'
        verbose_name_plural = 'اعضای خبرنامه'

    def __str__(self):
        return self.email

