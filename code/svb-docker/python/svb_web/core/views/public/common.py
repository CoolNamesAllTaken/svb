from django.shortcuts import render
import datetime
from zoneinfo import ZoneInfo
import math
import core.models


def calculate_historical_data_for_bank():
    historical_data_obligations = []
    historical_data_assets = []
    now = datetime.datetime.now(tz=ZoneInfo("America/Los_Angeles"))
    bank_reserve_account = core.models.Account.objects.get(account_number=0)
    assert bank_reserve_account.account_name == "RESERVES"
    night_start = core.models.AnchorEvent.objects.filter(account=bank_reserve_account,
                                                         category="CREATE_ACCOUNT"
                                                         ).first().timestamp
    BALANCE_CALCULATION_INTERVAL_SECONDS = 1800
    seconds_since_start = (now - night_start).total_seconds()
    intervals_since_start = range(math.floor(seconds_since_start / BALANCE_CALCULATION_INTERVAL_SECONDS) + 2)
    accounts = core.models.Account.objects.exclude(account_number=bank_reserve_account.account_number).all()
    for interval in intervals_since_start:
        interval_start = night_start + datetime.timedelta(seconds=BALANCE_CALCULATION_INTERVAL_SECONDS * interval)
        bank_summed_account_balances_at_interval_start = 0
        for account in accounts:
            bank_summed_account_balances_at_interval_start += account.get_balance(interval_start)
        historical_data_obligations.append({
            "x": datetime.datetime.timestamp(interval_start),
            "y": bank_summed_account_balances_at_interval_start,
        })
        candy_reserve_at_interval_start = bank_reserve_account.get_balance(interval_start)
        historical_data_assets.append({
            "x": datetime.datetime.timestamp(interval_start),
            "y": candy_reserve_at_interval_start,
        })
    return historical_data_obligations, historical_data_assets

# Create your views here.
def index(request):
    current_eek_level = core.models.BankState.objects.latest("timestamp").eek_level
    articles = core.models.NewsArticle.objects.filter(eek_level__lte=current_eek_level).order_by("-eek_level")
    # Could take just the most recent three but this is good for now.
    historical_obligations, historical_assets = calculate_historical_data_for_bank()
    context = {
                "articles": articles,
                "historical_obligations": historical_obligations,
                "historical_assets": historical_assets,
               }
    return render(request, "public/index.html", context)