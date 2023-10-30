from django.shortcuts import render, get_object_or_404
import datetime
import core.models

def calculate_historical_data_from_anchor_events(anchor_events: list[core.models.AnchorEvent]):
    historical_data = []
    for event in anchor_events:
        historical_data.append({
            "x": datetime.datetime.timestamp(event.timestamp),
            "y": event.balance,
        })
    return historical_data

# Create your views here.
def account(request, account_number=None):
    context = {}
    if account_number:
        account = get_object_or_404(core.models.Account, account_number=account_number)
        account_anchor_events = core.models.AnchorEvent.objects.filter(account=account)
        last_anchor_event = account_anchor_events.latest("timestamp")
        context = {
                    "account": account,
                    "anchor_event_history_data": calculate_historical_data_from_anchor_events(account_anchor_events),
                    "last_anchor_event": last_anchor_event,
                    "js_interest_rate": last_anchor_event.interest_rate,
                    "js_last_anchor_event_balance": last_anchor_event.balance,
                    "js_last_anchor_event_timestamp": last_anchor_event.timestamp.timestamp()}
    return render(request, "public/account.html", context)


def overview(request, customer_id=None):
    context = {}
    if customer_id:
        customer = get_object_or_404(core.models.Customer, customer_id=customer_id)
        context = {"customer": customer,
                   "accounts": [{
                                    "account_number": account.account_number,
                                    "anchor_event_history_data": calculate_historical_data_from_anchor_events(core.models.AnchorEvent.objects.filter(account=account)),
                                    "js_interest_rate": core.models.AnchorEvent.objects.filter(account=account).latest("timestamp").interest_rate,
                                    "js_last_anchor_event_balance": core.models.AnchorEvent.objects.filter(account=account).latest("timestamp").balance,
                                    "js_last_anchor_event_timestamp": core.models.AnchorEvent.objects.filter(account=account).latest("timestamp").timestamp.timestamp()
                        } for account in customer.account_set.all()]}
    return render(request, "public/customer.html", context)
