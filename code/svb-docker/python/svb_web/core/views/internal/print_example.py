from django.shortcuts import render
from core.models import ReceiptPrinter, Customer

def print_test(request):
    printer_names = [printer.name for printer in ReceiptPrinter.objects.all()]
    context = {
        "printer_names": printer_names,
        "customer_id": Customer.objects.all()[0].customer_id,
    }
    return render(request, "snippets/print_stub.html", context)
