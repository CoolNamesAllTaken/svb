from django.shortcuts import render
import datetime
from zoneinfo import ZoneInfo
import math
import core.models


def calculate_historical_data_for_bank():
    historical_data_obligations = []
    historical_data_assets = []
    now = datetime.datetime.now(tz=ZoneInfo("America/Los_Angeles"))
    BANK_ACCOUNT_ID = 7
    bank_reserve_account = core.models.Account.objects.get(account_number=BANK_ACCOUNT_ID)
    NIGHT_START = datetime.datetime(2023, 10, 28, hour=18, minute=0, second=0, microsecond=0,
                                    tzinfo=ZoneInfo("America/Los_Angeles"))
    # TODO: replace above constant with actual value from bank account model
    BALANCE_CALCULATION_INTERVAL_SECONDS = 1800
    seconds_since_start = (now - NIGHT_START).total_seconds()
    intervals_since_start = range(math.floor(seconds_since_start / BALANCE_CALCULATION_INTERVAL_SECONDS) + 2)
    accounts = core.models.Account.objects.exclude(account_number=BANK_ACCOUNT_ID).all()
    for interval in intervals_since_start:
        interval_start = NIGHT_START + datetime.timedelta(seconds=BALANCE_CALCULATION_INTERVAL_SECONDS * interval)
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
    articles = core.models.NewsArticle.objects.all()
    historical_obligations, historical_assets = calculate_historical_data_for_bank()
    context = {
                "articles": articles,
                "historical_obligations": historical_obligations,
                "historical_assets": historical_assets,
               }
    return render(request, "public/index.html", context)