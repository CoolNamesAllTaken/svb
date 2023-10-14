from django.shortcuts import render
from core.models import NewsArticle


def article(request, article_headline=None):
    # TODO: if article_headline is None, some kind of 404
    try:
        article = NewsArticle.objects.get(headline=article_headline)
    except NewsArticle.DoesNotExist:
        article = None
    context = {
        'article': article,
    }
    return render(request, 'article.html', context=context)
