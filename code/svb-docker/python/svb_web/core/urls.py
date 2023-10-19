from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.public.common.index, name="index"),
    path('account_holder/<int:account_holder_number>', views.public.customer.overview, name="account_holder"),
    path('account_holder', views.public.customer.overview, name="account_holder_generic"),
    path('account/<int:account_number>', views.public.customer.account, name="account"),
    path('account', views.public.customer.account, name="account_generic"),
    path('news_editor/', views.internal.author.news_editor),
    path('article/<str:article_headline>/', views.public.visitor.article, name='article'),
]
