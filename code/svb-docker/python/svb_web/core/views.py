from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context)

def account(request, account_number=None):
    context = {}
    return render(request, "account.html", context)