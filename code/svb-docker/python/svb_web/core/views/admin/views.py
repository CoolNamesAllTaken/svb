from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from core.utils.news_feed import get_all_newsfeed, get_live_newsfeed
from core.forms import AuthorForm, ArticleForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie


# @login_required
@ensure_csrf_cookie
def news_editor(request):
    if request.method == 'POST':
        request_action = request.POST['action']
        if request_action == 'create-author':
            form = AuthorForm(request.POST)
            if form.is_valid():
                author = form.save()
                messages.success(request, f'Author {author.name} created successfully')
        elif request_action == 'create-article':
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save()
                messages.success(request, f'Article "{article.headline}" created successfully')
    # if POST
    #   handle publish/unpublish requests
    # get news feeds, add to context
    live_news_feed = get_all_newsfeed()
    news_feed = get_live_newsfeed()
    author_form = AuthorForm()
    article_form = ArticleForm()
    context = {
        'articles': live_news_feed,
        'news_feed': news_feed,
        'author_form': author_form,
        'article_form': article_form,
    }
    return render(request, 'news_editor.html', context=context)


def account(request, account_number=None):
    context = {}
    return render(request, "account.html", context)
