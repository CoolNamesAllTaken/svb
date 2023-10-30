from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import core.models
import core.forms


def initialize_bank(request):
    messages = []
    bank_state = core.models.BankState.objects.all()
    if len(bank_state) == 0:
        initial_bank_state = core.models.BankState(eek_level=0)
        initial_bank_state.save()
    try:
        reserves = core.models.Account.objects.get(account_name="RESERVES")
    except core.models.Account.DoesNotExist:
        reserves = core.models.Account(pk=0, account_name="RESERVES")
        reserves.save()
        balance = request.POST['initial_bank_reserves']
        reserves.init(balance=balance)
        messages.append(f"Created account 'reserves' with balance {balance}.")
    else:
        messages.append("Account 'reserves' already exists.")
    try:
        disbursed = core.models.Account.objects.get(account_name="DISBURSED")
    except core.models.Account.DoesNotExist:
        disbursed = core.models.Account(pk=1, account_name="DISBURSED")
        disbursed.save()
        disbursed.init(balance=0)
        messages.append("Created account 'disbursed'.")
    else:
        messages.append("Account 'disbursed' already exists.")
    return messages


def freeze_rates(request):
    accounts = core.models.Account.objects.all()
    for account in accounts:
        account.set_interest_rate(0)
    return [f"Set interest rates to 0 for {len(accounts)} accounts."]


def update_rates(request):
    new_interest_rate = request.POST['new_interest_rate']
    accounts = core.models.Account.objects.exclude(account_name="RESERVES")\
        .exclude(account_name="DISBURSED").all()
    for account in accounts:
        account.set_interest_rate(new_interest_rate)
    return [f"Set interest rates to {new_interest_rate} for {len(accounts)} accounts."]


def set_eek_level(request):
    new_eek_level = request.POST['new_eek_level']
    # TODO: The below line likely to evolve as eek level does.
    bank_state = core.models.BankState.objects.latest("timestamp")
    if bank_state.eek_level != new_eek_level:
         core.models.BankState(eek_level=new_eek_level).save()
    return [f"Set current eek level to {new_eek_level}."]


def manage_bank(request):
    action = request.POST['action']
    if action == 'initialize-bank':
        return initialize_bank(request)
    elif action == "freeze-rates":
        return freeze_rates(request)
    elif action == "update-rates":
        return update_rates(request)
    elif action == "set-eek-level":
        return set_eek_level(request)

@login_required
def management(request):
    messages = []
    if request.method == 'POST':
        if 'action' in request.POST:
            messages = manage_bank(request)
    context = {
        "messages": messages,
        "initialize_bank_form": core.forms.InitializeBankForm(initial={'initial_bank_reserves': 1000}),
        "freeze_interest_rates_form": core.forms.FreezeRatesBankForm(),
        "update_interest_rates_form": core.forms.UpdateRatesBankForm(),
        "set_eek_level_form": core.forms.SetEekLevelBankForm(),
        }
    return render(request, "internal/management.html", context)
