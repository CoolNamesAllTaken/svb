from django.db import models
# from datetime import 

class IdCardPrintJob(models.Model):
    pass

class AccountHolder(models.Model):
    account_holder_number = models.AutoField(primary_key=True)
    first_name = models.CharField(default="Edween")
    costume = models.CharField(default="Founder")
    referrer_account_holder = models.ForeignKey(
        "AccountHolder",
        blank=True,
        null=True,
        on_delete=models.SET_NULL # make referrer field null if the referrer AccountHolder gets deleted
    )

class Account(models.Model):
    account_number = models.AutoField(primary_key=True)
    account_holder = models.ForeignKey(
        "AccountHolder",
        on_delete=models.CASCADE # delete Account when associated AccountHolder is deleted
    )
    interest_rate = models.FloatField()
    # Anchor Events:
    # - Interest rate changed.
    # - Cendy deposited into account.
    # - Candy withdrawn from account.
    #
    # Account balance at current timestamp can be calculatecd from previous anchor event timestamp and anchor event account balance.
    last_anchor_event_timestamp = models.DateTimeField(auto_now=True) # timestamp of last anchor event
    last_anchor_event_balance = models.DecimalField(decimal_places=3, max_digits=10) # account balance immediately after last anchor event


