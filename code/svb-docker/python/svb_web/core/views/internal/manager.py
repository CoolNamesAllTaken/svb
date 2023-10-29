from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def management(request):
    context = {}
    return render(request, "internal/management.html", context)