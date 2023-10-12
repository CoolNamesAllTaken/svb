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
    author = NewsAuthor.objects.get(id=author_name)
    article = NewsArticle(headline=headline, author=author)
    article.save()
    return article.id


def publish_article(article_id: str, publish_at: datetime = None):
    # if no publish_at provided, publish article now
    # set article publish time
    pass


def unpublish_article(article_id: str):
    # set article publish time to None
    pass
