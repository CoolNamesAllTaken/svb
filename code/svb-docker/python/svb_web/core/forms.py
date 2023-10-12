from django import forms
from core.models import NewsArticle, NewsAuthor


class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']
