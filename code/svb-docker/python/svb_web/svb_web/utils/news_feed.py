import datetime


def get_all_newsfeed():
    # return a list of articles in order of publish time
    pass


def get_live_newsfeed():
    # return a list of articles with publish time in the past in order of publish time
    pass


def create_article(headline: str, author_id: str):
    # create a new article
    pass


def publish_article(article_id: str, publish_at: datetime = None):
    # if no publish_at provided, publish article now
    # set article publish time
    pass


def unpublish_article(article_id: str):
    # set article publish time to None
    pass
