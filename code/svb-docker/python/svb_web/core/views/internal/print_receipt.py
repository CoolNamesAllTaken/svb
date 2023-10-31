from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import ReceiptPrinter, Customer, AnchorEvent, Account
from core.utils.time import get_timestamp_from_utc_str

@login_required
def print_receipt(request):
    print(request)
    printer_name = request.POST["printer_name"]
    customer_id = request.POST["customer_id"]
    receipt_type = request.POST["receipt_type"]
    # Timestamp is when the view that sent this POST request was rendered.
    # Used as a hacky way to find the latest anchor event.
    receipt_timestamp = get_timestamp_from_utc_str(request.POST["receipt_timestamp"])
    receipt_printer = get_object_or_404(ReceiptPrinter, name=printer_name)
    customer = get_object_or_404(Customer, customer_id=customer_id)

    receipt_printer.connect()
    if receipt_type == "new_customer":
        receipt_printer.print_new_customer_receipt(customer)
    else:
        receipt_printer.print_transaction_receipt(Account.objects.get(customer=customer).get_last_anchor_event(receipt_timestamp))
    return HttpResponse(status=204)  # do not redirect or otherwise change client state