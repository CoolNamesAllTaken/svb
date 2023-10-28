from django.shortcuts import render
from core.models import ReceiptPrinter

def print_test(request):

    printer_names = [printer.name for printer in ReceiptPrinter.objects.all()]
    context = {"printer_names": printer_names}
    return render(request, "internal/print_stub.html", context)