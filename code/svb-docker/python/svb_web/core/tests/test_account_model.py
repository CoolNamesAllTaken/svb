import pytest

from core.models import Customer, Account, AnchorEvent
from datetime import datetime, timedelta

@pytest.mark.django_db
def testaccount_create_delete():
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
    assert(Account.objects.filter(account_name__exact="test1")[0] == account1)
    # Test that accounts can be deleted.
    account1.delete()
    assert(len(Account.objects.filter(account_name__exact="test1")) == 0)
    
    # Reset database to original state.
    account2.delete()

@pytest.mark.django_db
def test_account_init_delete():
    account1 = Account(
        account_name="test1",
        customer=None
    )
    account1.save()
    # Account not yet initialized, there should be no associated anchor events.
    assert(len(AnchorEvent.objects.filter(account__exact=account1)) == 0)
    
    # Test that account can't be initialized in the future.
    with pytest.raises(ValueError):
        account1.init(init_timestamp=datetime.now()+timedelta(minutes=10))
    # Initialize the account.
    init_anchor_event = account1.init()
    assert(AnchorEvent.objects.get(pk=init_anchor_event.pk) != None)
    assert(len(AnchorEvent.objects.filter(pk__exact=init_anchor_event.pk))==1)
    # Test that account can't be initialized twice.
    with pytest.raises(RuntimeError):
        account1.init()
    
    # Delete the initialization AnchorEvent and init with new parameters.
    init_anchor_event.delete()
    assert(len(AnchorEvent.objects.filter(pk__exact=init_anchor_event.pk))==0)
    # Should be able to init again now that first anchor event is gone.
    init_timestamp=datetime.now()
    init_anchor_event = account1.init(
        init_timestamp=init_timestamp,
        init_balance=100.3,
        init_interest_rate=3
    )
    matched_init_anchor_events = AnchorEvent.objects.filter(account__exact=account1)
    assert(len(matched_init_anchor_events) == 1)
    retrieved_init_anchor_event = matched_init_anchor_events[0]
    assert(retrieved_init_anchor_event.timestamp == init_anchor_event.timestamp)
    # Cast these both to floats since Balance is a Decimal to avoid floating point error
    # and now it bite us in the butt.
    assert(float(retrieved_init_anchor_event.balance) == float(init_anchor_event.balance))
    assert(retrieved_init_anchor_event.interest_rate == init_anchor_event.interest_rate)

    # Delete the account and make sure the corresponding AnchorEvents are gone.
    account1.delete()
    assert(len(AnchorEvent.objects.filter(account__exact=account1.pk)) == 0)


# @pytest.mark.django_db
# def test_account_transfer():
#     account1 = Account(
#         account_name="test1",
#         customer=None
#     )
#     account2 = Account(
#         account_name="test2",
#         customer=None
#     )
#     account1.save()
#     account2.save()

#     account1.transfer_funds()