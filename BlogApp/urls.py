from django.urls import path, re_path
from . import views

app_name = 'BlogApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles_list, name='article_list'),
    re_path(r'detail/(?P<slug>[-\w]+)/', views.article_detail, name='article_detail'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.category_article, name='category_article'),
    re_path(r'tag/(?P<slug>[-\w]+)/', views.tag_article, name='tag_article'),
    path('search/', views.search, name='search_article'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe'),
    re_path(r'like/(?P<slug>[-\w]+)/', views.LikeView.as_view(), name='like'),
]
