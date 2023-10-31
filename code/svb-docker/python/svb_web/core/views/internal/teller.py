from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from core.models import Customer, Account, ReceiptPrinter
from django.contrib.auth.decorators import login_required
import core.forms

@login_required
def lookup_accounts(request, customer_id=None):
    """
    @brief View function that allows looking up a Customer's accounts using their customer ID.
    @param[in] customer_id ID of a customer from a previous failed lookup. Correct lookups
        should result in a redirect, so we don't expect them to go back to this view
        function.
    """
    message = "Lookup customer by ID."
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = core.forms.CustomerLookupForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            customer_id = form.cleaned_data['customer_id']
            try:
                customer = get_object_or_404(Customer, pk=customer_id)
                # redirect to a new URL:
                return HttpResponseRedirect('/internal/accounts/edit/' + customer_id + '/')
            except:
                message = "Customer ID {} not found!".format(customer_id)
        else:
            message = "Form contents not valid. Try again!"
    else:
        form = core.forms.CustomerLookupForm()
    
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, "internal/lookup_accounts.html", context)


def make_withdrawal(request):
    form_account_number = request.POST['account_number']
    withdrawal_amount = int(request.POST['withdrawal_amount'])
    account_to_withdraw_from = Account.objects.get(account_number=form_account_number)
    bank_reserve_account = Account.objects.get(account_name="RESERVES")
    bank_disbursed_account = Account.objects.get(account_name="DISBURSED")
    success = Account.transfer_funds(account_to_withdraw_from, bank_disbursed_account, withdrawal_amount)
    if success:
        # This could possibly create a race condition
        current_reserves = bank_reserve_account.get_balance()
        core.models.AnchorEvent(account=bank_reserve_account, 
                                balance= current_reserves - withdrawal_amount,
                                category="WITHDRAWAL").save()
        return ["Account withdrawal succeeded."]
    else:
        return ["Account withdrawal failed."]


def teller_actions(request):
    action = request.POST['action']
    if action == 'make_withdrawal':
        return make_withdrawal(request)


@login_required
def edit_accounts(request, customer_id=None):
    # can assume customer_id is valid
    messages = []
    if request.method == 'POST':
        if 'action' in request.POST:
            messages = teller_actions(request)
    customer = Customer.objects.get(pk=customer_id)
    context = {
        "customer": customer,
        "messages": messages,
        "account_withdrawal_entries": [{
                                        "form": core.forms.MakeWithdrawalForm(initial={'account_number': account.account_number}),
                                        "account": account,
                                        "current_balance": account.get_balance()
         } for account in customer.account_set.all()],
        'printer_names': [printer.name for printer in ReceiptPrinter.objects.all()],
        'receipt_type': "transaction",
        'customer_id': customer.customer_id,
    }
    return render(request, "internal/teller.html", context)
