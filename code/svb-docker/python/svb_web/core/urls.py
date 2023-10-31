from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.public.common.index, name="index"),
    path('account/<int:account_number>/', views.public.customer.account, name="account"),
    path('account/', views.public.customer.account, name="account_generic"),
    path('customer/', views.public.customer.overview, name='customer_generic'),
    path('customer/<str:customer_id>/', views.public.customer.overview, name='customer'),
    path('c/<str:customer_id>/', views.public.customer.overview, name='customer'),
    path('article/<str:article_headline>/', views.public.visitor.article, name='article'),
    path('internal/', views.internal.common.index, name='internal_index'),
    path('internal/news_editor/', views.internal.author.news_editor),
    path('internal/print_debit_card/<str:customer_id>/', views.internal.banker.print_debit_card, name='print_debit_card'),
    path('internal/print_receipt/', views.internal.print_receipt.print_receipt, name="print_receipt"),
    path('internal/customer/create/', views.internal.banker.edit_customer, name='create_customer'),
    path('internal/customer/lookup/', views.internal.banker.lookup_customer, name='lookup_customer'),
    path('internal/customer/edit/<str:customer_id>/', views.internal.banker.edit_customer, name='edit_customer'),
    path('internal/accounts/lookup/', views.internal.teller.lookup_accounts, name='lookup_accounts'), 
    path('internal/accounts/edit/<str:customer_id>/', views.internal.teller.edit_accounts, name='edit_accounts'),
    path('internal/management/', views.internal.manager.management, name='management'),
    path('internal/', include("django.contrib.auth.urls")),
]
