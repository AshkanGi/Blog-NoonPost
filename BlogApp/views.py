from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Tag, Comment
from django.core.paginator import Paginator
from .forms import MessageForm, SubscriberForm
from AccountApp.models import User


def get_pages_to_show(current_page, total_pages):
    """Utility function to determine which pagination pages to show."""
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def home(request):
    popular_articles = Article.objects.filter(status=True).order_by('-view')[:3]
    programming_articles = Article.objects.filter(status=True, category__title='برنامه نویسی').order_by('-view')[:3]
    food_cooking_articles = Article.objects.filter(status=True, category__title='غذا و آشپزی').order_by('-view')[:3]
    sport_articles = Article.objects.filter(status=True, category__title='ورزشی').order_by('-view')[:3]
    return render(request, 'BlogApp/home.html', {'popular_articles': popular_articles, 'programming_articles': programming_articles,
                                                 'food_cooking_articles': food_cooking_articles, 'sport_articles': sport_articles})


def article_detail(request, slug):
    tag = Tag.objects.all()
    article = get_object_or_404(Article, slug=slug)
    # article.view += 1
    # article.save()
    if request.method == 'POST':
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user)
    return render(request, 'BlogApp/article_detail.html', {'tag': tag, 'article': article})


def articles_list(request):
    tag = Tag.objects.all()
    articles = Article.objects.filter(status=True)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'BlogApp/articles_list.html', {'tag': tag, 'articles': object_list, 'pages_to_show': pages_to_show})


def category_article(request, slug):
    tag = Tag.objects.all()
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(status=True, category=category)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'BlogApp/category_article.html', {'tag': tag, 'category': category, 'articles': object_list,
                                                             'pages_to_show': pages_to_show})


def tag_article(request, slug):
    tag = Tag.objects.all()
    tags = get_object_or_404(Tag, slug=slug)
    articles = tags.tags.all()
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'BlogApp/tag_article.html', {'tag': tag, 'tags': tags, 'articles': object_list, 'pages_to_show': pages_to_show})


def author_detail(request, author_id):
    author = get_object_or_404(User, id=author_id)
    articles = Article.objects.filter(status=True, author=author).order_by('-created_at')
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'BlogApp/author_detail.html', {'author': author, 'articles': object_list,
                                                          'pages_to_show': pages_to_show})


def search(request):
    tag = Tag.objects.all()
    search_article = request.GET.get('search')
    articles = Article.objects.filter(title__icontains=search_article)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'BlogApp/articles_list.html', {'tag': tag, 'articles': object_list, 'pages_to_show': pages_to_show})


def contact(request):
    tag = Tag.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('BlogApp:home')
    else:
        form = MessageForm()
    return render(request, 'BlogApp/contact.html', {'tag': tag, 'form': form})


def about(request):
    tag = Tag.objects.all()
    return render(request, 'BlogApp/about.html', {'tag': tag})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('BlogApp:home')
