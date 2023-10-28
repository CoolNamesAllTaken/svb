from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.utils.news_feed import get_all_newsfeed, get_live_newsfeed, publish_article, unpublish_article
from core.forms import AuthorForm, ArticleForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
def create_author_or_article(request):
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


@login_required
def toggle_publish_article(request):
    if 'publish' in request.POST:
        publish_article(request.POST['publish'])
        messages.success(request, f'Article "{request.POST["publish"]}" published successfully')
    else:
        unpublish_article(request.POST['unpublish'])
        messages.success(request, f'Article "{request.POST["unpublish"]}" unpublished successfully')


@login_required
@ensure_csrf_cookie
def news_editor(request):
    if request.method == 'POST':
        if 'action' in request.POST:
            create_author_or_article(request)
        else:
            toggle_publish_article(request)
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
    return render(request, 'internal/news_editor.html', context=context)
