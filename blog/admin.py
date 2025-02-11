from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    search_fields = ['title']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'view', 'article_image', 'created_at', 'status']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['title']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'fullname', 'subject', 'created_at']
    search_fields = ['email']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at', 'status']
    list_editable = ['status']
    search_fields = ['article']


@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    search_fields = ['user', 'article']
