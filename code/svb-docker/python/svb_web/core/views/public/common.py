from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        "num_ids_created": 0,
        "num_windows": 0,
        "wait_time": 0,
        "id_card_image_data": None,
    }
    return render(request, "public/index.html", context)