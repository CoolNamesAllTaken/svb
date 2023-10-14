from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.public.views.index, name="index"),
    path('account/', views.admin.articles.account, name="account"),
    path('news_editor/', views.admin.articles.news_editor)
]
