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
    # Account balance at current timestamp can be calculated from previous anchor event
    # timestamp and anchor event account balance.

    
class AnchorEvent(models.Model):
    # Anchor Events:
    # - Account created.
    # - Interest rate changed.
    # - Candy deposited into account.
    # - Candy withdrawn from account.
    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE # delete AccountTransaction when associated Account is deleted
    )
    category = models.CharField(max_length=64, blank=True, null=True)  # deposit, withdrawal, interest rate update
    timestamp = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(decimal_places=3, max_digits=10) # balance immediately after event
    interest_rate = models.FloatField(default=0.0) # 0.01 = 1%; default to 0 cuz WE decide when you get interest


class NewsAuthor(models.Model):
    name = models.CharField(max_length=32, unique=True)  # "Jane Doe"
    title = models.CharField(max_length=64, blank=True, null=True)  # "Candy QA"

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    headline = models.CharField(max_length=128, unique=True)  # "Shrinkflation: King Size Candy 20% Smaller"
    author = models.ForeignKey('NewsAuthor', on_delete=models.RESTRICT)
    date_published = models.DateTimeField(blank=True, null=True)
    preview = models.TextField(blank=True, null=True)  # "Candy companies are shrinking their products to save money. Is this a good thing?"
    body = models.TextField(blank=True, null=True)  # "Avid trick-or-treaters know the golden rule of treating: bigger is always better. <paragraphs of drivel>"

    def __str__(self):
        return f'"{self.headline}" by {self.author.name}'

    @property
    def is_published(self):
        return self.date_published is not None and datetime.datetime.now() > self.date_published
