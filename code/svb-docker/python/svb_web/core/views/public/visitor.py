from django.shortcuts import render
from core.models import NewsArticle
from core.utils.news_feed import get_live_newsfeed

def article(request, article_headline=None):
    # TODO: if article_headline is None, some kind of 404
    try:
        article = NewsArticle.objects.get(headline=article_headline)
    except NewsArticle.DoesNotExist:
        article = None

    context = {
        'articles': get_live_newsfeed(),
        'article': article,
    }
    return render(request, 'public/article.html', context=context)