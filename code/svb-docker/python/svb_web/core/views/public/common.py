from django.shortcuts import render
import core.models

# Create your views here.
def index(request):
    articles = core.models.NewsArticle.objects.all()
    context = {
                "articles": articles
               }
    return render(request, "public/index.html", context)