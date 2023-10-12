from django.db import models
import datetime


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
    
    # Anchor Events:
    # - Interest rate changed.
    # - Cendy deposited into account.
    # - Candy withdrawn from account.
    #
    # Account balance at current timestamp can be calculatecd from previous anchor event timestamp and anchor event account balance.
    last_anchor_event_timestamp = models.DateTimeField(auto_now=True) # timestamp of last anchor event
    last_anchor_event_balance = models.DecimalField(decimal_places=3, max_digits=10) # account balance immediately after last anchor event


class NewsAuthor(models.Model):
    name = models.CharField(max_length=32, unique=True)  # "Jane Doe"
    title = models.CharField(max_length=64, blank=True, null=True)  # "Candy QA"

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    headline = models.CharField(max_length=128, unique=True)  # "Shrinkflation: King Size Candy 20% Smaller"
    author = models.ForeignKey('NewsAuthor', on_delete=models.RESTRICT)
    date_published = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'"{self.headline}" by {self.author.name}'

    @property
    def is_published(self):
        return self.date_published is not None and datetime.datetime.now() > self.date_published
