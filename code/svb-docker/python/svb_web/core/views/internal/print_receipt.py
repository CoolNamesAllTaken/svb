from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import ReceiptPrinter, Customer


@login_required
def print_receipt(request):
    printer_name = request.POST["printer_name"]
    customer_id = request.POST["customer_id"]
    receipt_printer = get_object_or_404(ReceiptPrinter, name=printer_name)
    customer = get_object_or_404(Customer, customer_id=customer_id)

    receipt_printer.connect_to_printer()
    receipt_printer.print_transaction_receipt(customer)
    return HttpResponse(status=204)  # do not redirect or otherwise change client state