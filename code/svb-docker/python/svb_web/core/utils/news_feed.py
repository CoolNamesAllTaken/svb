import datetime
from models import NewsArticle, NewsAuthor


def get_all_newsfeed():
    # return a list of articles in order of publish time
    pass


def get_live_newsfeed():
    # return a list of articles with publish time in the past in order of publish time
    pass


def create_article(headline: str, author_name: str):
    # create a new article
    author = NewsAuthor.objects.get(name=author_name)
    article = NewsArticle(headline=headline, author=author)
    article.save()
    return article.headline


def publish_article(headline: str, publish_at: datetime = None):
    if publish_at is None:
        publish_at = datetime.datetime.now()
    article = NewsArticle.objects.get(headline=headline)
    article.date_published = publish_at
    article.save()
    return article.headline


def unpublish_article(headline: str):
    article = NewsArticle.objects.get(headline=headline)
    article.date_published = None
    article.save()
    return article.headline
