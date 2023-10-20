from django.db import models
from datetime import date


class IdCardPrintJob(models.Model):
    pass


class Customer(models.Model):
    kCustomerIdMaxLength = 12

    customer_id = models.CharField(default="TBA", max_length=kCustomerIdMaxLength, primary_key=True)
    first_name = models.CharField(default="Edween")
    costume = models.CharField(default="Founder")
    referrer_customer_id = models.ForeignKey(
        "Customer",
        blank=True, # allow empty fields in forms
        null=True, # allow NULL values in storage
        on_delete=models.SET_NULL # make referrer field null if the referrer AccountHolder gets deleted
    )
    joined_date = models.DateField(default=date.today)
    security_candy = models.CharField(default="")

def get_new_customer_id(first_name, costume):
    """
    @brief Generates a new customer ID based on name, costume, sequential order. Used by forms to generate new
    customer IDs as part of a cleaning function.
    @param[in] first_name First name of the customer.
    @param[in] costume Name of the customer's costume.
    """
    print(f"get_new_customer_id with first_name={first_name} costume={costume}")
    costume_name_prefix = first_name[0] + costume[0] # First letter of first name and costume name.
    print(f"costume_name_prefix={costume_name_prefix}")
    date_code = f"{date.today().year % 100}{date.today().month:0>2}{date.today().day}" # YYMMDD
    customer_counter = Customer.objects.filter(joined_date=date.today()).count()
    return f"{costume_name_prefix}{date_code}{customer_counter:0>4}" # this will break something after 9999 licenses in one day!

class Account(models.Model):
    account_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        "Customer",
        # Don't allow blank since forms creating an account must specify a customer.
        null=True, # allow NULL values in storage
        on_delete=models.CASCADE # delete Account when associated Customer is deleted
    )
    interest_rate = models.FloatField(default=0.0) # 0.01 = 1%; default to 0 cuz WE decide when you get interest
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
    preview = models.TextField(blank=True, null=True)  # "Candy companies are shrinking their products to save money. Is this a good thing?"
    body = models.TextField(blank=True, null=True)  # "Avid trick-or-treaters know the golden rule of treating: bigger is always better. <paragraphs of drivel>"

    def __str__(self):
        return f'"{self.headline}" by {self.author.name}'

    @property
    def is_published(self):
        return self.date_published is not None and datetime.datetime.now() > self.date_published
