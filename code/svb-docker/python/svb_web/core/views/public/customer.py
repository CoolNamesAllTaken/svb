from django.shortcuts import render, get_object_or_404
import core.models

# Create your views here.
def account(request, account_number=None):
    context = {}
    if account_number:
        account = get_object_or_404(core.models.Account, account_number=account_number)
        last_anchor_event = core.models.AnchorEvent.objects.filter(account=account).latest("timestamp")
        context = {
                    "account": account,
                    "last_anchor_event": last_anchor_event,
                    "js_interest_rate": last_anchor_event.interest_rate,
                    "js_last_anchor_event_balance": last_anchor_event.balance,
                    "js_last_anchor_event_timestamp": last_anchor_event.timestamp.timestamp()}
    return render(request, "account.html", context)


def overview(request, account_holder_number=None):
    context = {}
    if account_holder_number:
        account_holder = get_object_or_404(core.models.AccountHolder, account_holder_number=account_holder_number)
        context = {"account_holder": account_holder}
    return render(request, "account_holder.html", context)
