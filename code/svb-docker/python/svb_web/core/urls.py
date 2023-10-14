from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account"),
    path('news_editor/', views.news_editor),
    path('article/<str:article_headline>/', views.article, name='article'),
]
