from django.shortcuts import render

# Create your views here.
def view_accounts(request, customer_id=None):
    context = {}
    return render(request, "account.html", context)
