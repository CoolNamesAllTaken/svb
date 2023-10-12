from django.shortcuts import render

# Create your views here.
def account(request, account_number=None):
    context = {}
    return render(request, "account.html", context)