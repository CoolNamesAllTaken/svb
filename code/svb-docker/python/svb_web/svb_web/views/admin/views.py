from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# @login_required
def news_editor(request):
    # if POST
    #   handle publish/unpublish requests
    # get news feeds, add to context
    context = {}
    return render(request, 'svb_web/news_editor.html', context=context)
