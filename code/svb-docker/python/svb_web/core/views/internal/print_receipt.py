from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from core.models import ReceiptPrinter, Account

def print_receipt(request):
    # if not a visible view, maybe should fail silently?
    # if no choice selected, and press print (who is responsible for updating the form?)
    receipt_printer = get_object_or_404(ReceiptPrinter, name=request.POST["printer_name"])
    customer_account = get_object_or_404(Account, account_number=request.POST["account_number"])
    receipt_printer.connect_to_printer()
    receipt_type = request.POST["receipt_type"]
    if receipt_type == "deposit":
        receipt_printer.print_deposit_receipt(customer_account)
    elif receipt_type == "withdrawal":
        receipt_printer.print_withdrawal_receipt(customer_account)
    else:
        return HttpResponseBadRequest("Invalid receipt type in POST request")
    return HttpResponse(status=204)  # do not redirect or otherwise change client state