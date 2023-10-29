import pytest
import core.models as models
import datetime
import django.utils.timezone


class TestAccountGetBalance:

    @pytest.mark.django_db
    def test_get_balance_calculates_current_balance_no_interest(self, monkeypatch):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        account = models.Account(account_number=1)
        account.save()
        two_hours_ago = (now - datetime.timedelta(hours=2))
        monkeypatch.setattr(django.utils.timezone, 'now', lambda: two_hours_ago)
        initial_anchor_event = models.AnchorEvent(account=account, category="initial",
                                                  timestamp=two_hours_ago,
                                                  balance=2, interest_rate=0)
        initial_anchor_event.save()
        account_balance_calculated = account.get_balance(now)
        assert account_balance_calculated == initial_anchor_event.balance

    @pytest.mark.django_db
    def test_get_balance_calculates_current_balance_with_interest(self, monkeypatch):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        account = models.Account(account_number=1)
        account.save()
        two_hours_ago = (now - datetime.timedelta(hours=2))
        monkeypatch.setattr(django.utils.timezone, 'now', lambda: two_hours_ago)
        initial_anchor_event = models.AnchorEvent(account=account, category="initial",
                                                  timestamp=two_hours_ago,
                                                  balance=2, interest_rate=0.5)
        initial_anchor_event.save()
        account_balance_calculated = account.get_balance(now)
        assert account_balance_calculated == pytest.approx(14.8, 0.05)

    @pytest.mark.django_db
    def test_get_balance_with_two_anchor_events(self, monkeypatch):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        account = models.Account(account_number=1)
        account.save()
        two_hours_ago = (now - datetime.timedelta(hours=2))
        monkeypatch.setattr(django.utils.timezone, 'now', lambda: two_hours_ago)
        initial_anchor_event = models.AnchorEvent(account=account, category="initial",
                                                  timestamp=two_hours_ago,
                                                  balance=2, interest_rate=0.5)
        initial_anchor_event.save()
        one_hour_ago = (now - datetime.timedelta(hours=1))
        monkeypatch.setattr(django.utils.timezone, 'now', lambda: one_hour_ago)
        initial_anchor_event = models.AnchorEvent(account=account, category="update",
                                                  timestamp=one_hour_ago,
                                                  balance=100, interest_rate=0.0)
        initial_anchor_event.save()
        account_balance_calculated_now = account.get_balance(now)
        assert account_balance_calculated_now == 100
        just_before_one_hour_ago = one_hour_ago = (now - datetime.timedelta(minutes=61))
        account_balance_just_before_update = account.get_balance(just_before_one_hour_ago)
        assert account_balance_just_before_update == pytest.approx(5.35, 0.05)
