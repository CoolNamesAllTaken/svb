'''
WARNING: hacky testing purposes only
please remove this as soon as possible.
'''
from django.http import HttpResponse

def populate_db(request):
    #############################
    from core.models import Customer
    customer_one = Customer(
        first_name="first name 1",
        costume="costume 1",
        referrer=None,
        security_candy="security candy 1",
    )
    customer_one.save()
    customer_two = Customer(
        first_name="first name 2",
        costume="costume 2",
        referrer=customer_one,
        security_candy="security candy 2",
    )
    customer_two.save()
    #############################
    from core.models import Account
    account_one = Account(
        customer=customer_one
    )
    account_one.save()
    account_two = Account(
        customer=customer_two
    )
    account_two.save()
    #############################
    from core.models import ReceiptPrinter
    rp_one = ReceiptPrinter(
        name="rp one",
        ip_address="10.3.2.178"
    )
    rp_one.save()
    rp_two = ReceiptPrinter(
        name="rp two",
        ip_address="10.3.2.149"
    )
    rp_two.save()
    rp_three = ReceiptPrinter(
        name="rp three",
        ip_address="10.3.2.156"
    )
    rp_three.save()
    #############################
    return HttpResponse()
