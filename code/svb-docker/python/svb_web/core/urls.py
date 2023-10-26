from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.public.common.index, name="index"),
    path('account/', views.public.customer.account, name="view_account"),
    path('article/<str:article_headline>/', views.public.visitor.article, name='article'),
    path('internal/news_editor/', views.internal.author.news_editor),
    path('internal/customer/create/', views.internal.banker.edit_customer, name='create_customer'),
    path('internal/customer/edit/<str:customer_id>/', views.internal.banker.edit_customer, name='edit_customer'),
    # path('internal/account/lookup', views.internal.banker.lookup_account, name='lookup_account'),
    # path('internal/account/edit', views.internal.banker.edit_account, name='edit_account'),
    path('internal/print_test', views.internal.print_test.print_test, name="print_test"),
    path('internal/print_receipt', views.internal.print_receipt.print_receipt, name="print_receipt")
]
