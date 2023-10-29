import pytest, time

from core.models import Customer, Account, AnchorEvent
from datetime import datetime, timedelta, timezone

@pytest.mark.django_db
def test_account_create_delete():
    customer = Customer(
        customer_id="test_cust",
        first_name="frank",
        costume="lyboring",
        referrer=None,
        security_candy="toots"
    )
    account1 = Account(
        account_name="test1",
        customer=None
    )
    account2 = Account(
        account_name="test2",
        customer=None
    )
    account1.save()
    account2.save()

    # Test that account numbers are incrementing properly.
    assert account1.account_number < account2.account_number
    # Test that accounts can be retrieved by name.
    assert Account.objects.filter(account_name__exact="test1")[0] == account1
    # Test that accounts can be deleted.
    account1.delete()
    assert len(Account.objects.filter(account_name__exact="test1")) == 0

@pytest.mark.django_db
def test_account_init_delete():
    account1 = Account(
        account_name="test1",
        customer=None
    )
    account1.save()
    # Account not yet initialized, there should be no associated anchor events.
    assert len(AnchorEvent.objects.filter(account__exact=account1)) == 0
    
    # Test that account can't be initialized in the future.
    with pytest.raises(ValueError):
        account1.init(timestamp=datetime.now(tz=timezone.utc)+timedelta(minutes=10))
    # Initialize the account.
    init_anchor_event = account1.init()
    assert AnchorEvent.objects.get(pk=init_anchor_event.pk) != None
    assert len(AnchorEvent.objects.filter(pk__exact=init_anchor_event.pk))==1
    # Test that account can't be initialized twice.
    with pytest.raises(RuntimeError):
        account1.init()
    
    # Delete the initialization AnchorEvent and init with new parameters.
    init_anchor_event.delete()
    assert len(AnchorEvent.objects.filter(pk__exact=init_anchor_event.pk))==0
    # Should be able to init again now that first anchor event is gone.
    init_timestamp=datetime.now(tz=timezone.utc)
    init_anchor_event = account1.init(
        timestamp=init_timestamp,
        balance=100.3,
        interest_rate=3
    )
    matched_init_anchor_events = AnchorEvent.objects.filter(account__exact=account1)
    assert len(matched_init_anchor_events) == 1
    retrieved_init_anchor_event = matched_init_anchor_events[0]
    assert(retrieved_init_anchor_event.timestamp == init_anchor_event.timestamp)
    # Cast these both to floats since Balance is a Decimal to avoid floating point error
    # and it is still the right choice for a legitimate financial institution like ours.

    assert float(retrieved_init_anchor_event.balance) == float(init_anchor_event.balance)
    assert retrieved_init_anchor_event.interest_rate == init_anchor_event.interest_rate

    # Delete the account and make sure the corresponding AnchorEvents are gone.
    account1.delete()
    assert len(AnchorEvent.objects.filter(account__exact=account1.pk)) == 0

@pytest.mark.django_db
def test_account_interest_rate():
    test_account = Account()
    test_account.save()
    # Can't ask for interest rate before the account is initialized.
    with pytest.raises(RuntimeError):
        test_account.get_interest_rate()
    # Also can't set interest rate before the account is initiated.
    with pytest.raises(RuntimeError):
        test_account.set_interest_rate(9.0)
    test_account.init()
    test_account.set_interest_rate(5.3)
    assert test_account.get_interest_rate() == 5.3
    saved_timestamp = datetime.now(tz=timezone.utc) # save this for later
    # Set and get a new interest rate.
    time.sleep(0.1) # wait for a new timestamp to occur
    test_account.set_interest_rate(2.0)
    assert test_account.get_interest_rate() == 2.0
    # Now see if we can recall the interest rate in the past.
    assert test_account.get_interest_rate(timestamp=saved_timestamp) == 5.3
    test_account.delete()

@pytest.mark.django_db
def test_account_transfer():
    account1 = Account(
        account_name="test1",
        customer=None
    )
    account2 = Account(
        account_name="test2",
        customer=None
    )
    account1.save()
    account2.save()

    # Check that we can't transfer funds between non-initialized accounts.
    with pytest.raises(RuntimeError):
        Account.transfer_funds(account1, account2, 5)
        Account.transfer_funds(account2, account1, 3)

    account1.init(
        balance=6
    )

    # Check that we still can't transfer funds if one of the accounts is not initialized.
    with pytest.raises(RuntimeError):
        Account.transfer_funds(account1, account2, 5)
        Account.transfer_funds(account2, account1, 3)

    account2.init(
        balance=2
    )

    assert account1.get_balance() == 6
    assert account2.get_balance() == 2
    # Transfer should fail due to insufficient balance.
    assert not Account.transfer_funds(account1, account2, 80)
    assert account1.get_balance() == 6
    assert account2.get_balance() == 2
    # Transfer should succeed.
    assert Account.transfer_funds(account1, account2, 1)
    assert account1.get_balance() == 5
    assert account2.get_balance() == 3
    # Do fast transfers to make sure overwriting of most recent anchor events with identical
    # timestamps is working properly.
    assert Account.transfer_funds(account1, account2, 1)
    assert Account.transfer_funds(account1, account2, 1)
    assert Account.transfer_funds(account1, account2, 1)
    assert account1.get_balance() == 2
    assert account2.get_balance() == 6