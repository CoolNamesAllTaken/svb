from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
     path('', views.public.common.index, name="index"),
    path('account/', views.public.customer.account, name="account"),
    path('news_editor/', views.internal.author.news_editor),
    path('article/<str:article_headline>/', views.public.visitor.article, name='article'),
]
