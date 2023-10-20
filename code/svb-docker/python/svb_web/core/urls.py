from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.public.common.index, name="index"),
    path('account/<int:account_number>', views.public.customer.account, name="account"),
    path('account', views.public.customer.account, name="account_generic"),
    path('article/<str:article_headline>/', views.public.visitor.article, name='article'),
    path('internal/', views.internal.common.index, name='internal_index'),
    path('internal/news_editor/', views.internal.author.news_editor),
    path('internal/customer/create/', views.internal.banker.edit_customer, name='internal_create_customer'),
    path('internal/customer/lookup/', views.internal.banker.lookup_customer, name='internal_lookup_customer'),
    path('internal/customer/edit/<str:customer_id>/', views.internal.banker.edit_customer, name='internal_edit_customer'),
    # path('internal/manage/')
]
