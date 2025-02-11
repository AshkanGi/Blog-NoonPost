from blog.models import Article, Category


def articles_categories(request):
    latest_articles = Article.objects.filter(status=True).order_by('-created_at')[:4]
    categories = Category.objects.filter(status=True)

    return {'latest_articles': latest_articles, 'categories': categories}
