from django.db import models
from datetime import date
import datetime
import escpos.printer
import math


class IdCardPrintJob(models.Model):
    pass


class Customer(models.Model):
    def __str__(self) -> str:
        """
        @brief Override default tostring function so that it prints a nice ID string.
        @retval customer_id as a string.
        """
        return self.customer_id

    def get_customer_id(self):
        """
        @brief Generates a new customer ID based on name, costume, sequential order. Used by the
        overridden Customer.save() function when saving an instance of the Customer model.
        """
        print(f"get_customer_id with first_name={self.first_name} costume={self.costume}")
        costume_name_prefix = self.first_name[0] + self.costume[0] # First letter of first name and costume name.
        print(f"costume_name_prefix={costume_name_prefix}")
        date_code = f"{date.today().year % 100}{date.today().month:0>2}{date.today().day}" # YYMMDD
        customer_counter = Customer.objects.filter(joined_date=date.today()).count()
        return f"{costume_name_prefix}{date_code}{customer_counter:0>4}" # this will break something after 9999 licenses in one day!

    def save(self, *args, **kwargs):
        """
        @brief Override the model save function to create the new customer ID from first name, costume, and timestamp.
        """
        if self.customer_id == "TBA":
            # Customer object is being saved for the first time.
            self.customer_id = self.get_customer_id()
        super(Customer, self).save(*args, **kwargs) # call super save function

    # Constants
    CUSTOMER_ID_MAX_LENGTH = 12 # maximum number of characters for customer_id

    # Model Parameters
    customer_id = models.CharField(default="TBA", max_length=CUSTOMER_ID_MAX_LENGTH, primary_key=True)
    first_name = models.CharField(default="Edween", max_length=64)
    costume = models.CharField(default="Founder", max_length=64)
    referrer = models.ForeignKey(
        "Customer",
        blank=True, # allow empty fields in forms
        null=True, # allow NULL values in storage
        on_delete=models.SET_NULL # make referrer field null if the referrer AccountHolder gets deleted
    )
    joined_date = models.DateField(default=date.today)
    security_candy = models.CharField(default="", max_length=64)



class Account(models.Model):
    account_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        "Customer",
        # Don't allow blank since forms creating an account must specify a customer.
        null=True, # allow NULL values in storage
        on_delete=models.CASCADE # delete Account when associated Customer is deleted
    )
    # Account balance at current timestamp can be calculated from previous anchor event
    # timestamp and anchor event account balance.
    def get_balance(self, timestamp):
        """
        @brief Returns the balance of the account at the given timestamp. Backdates to the last anchor event.
        And calculates the interest accrued since then.
        @param[in] timestamp Datetime timestamp to calculate interest at.
        @retval Account balance at the specified timestamp.
        """
        COMPOUNDING_INTERVAL_SECONDS = 1800
        events_before_timestamp = AnchorEvent.objects.filter(account=self,
                                                                    timestamp__lte=timestamp)
        if events_before_timestamp:
            most_recent_event_at_timestamp = events_before_timestamp.latest("timestamp")
            interest_rate = most_recent_event_at_timestamp.interest_rate
            anchor_event_timestamp = most_recent_event_at_timestamp.timestamp
            anchor_event_balance = most_recent_event_at_timestamp.balance
            intervals_since_anchor_event = (timestamp - anchor_event_timestamp).total_seconds() / COMPOUNDING_INTERVAL_SECONDS
            balance_at_timestamp = float(anchor_event_balance) * math.exp(interest_rate * intervals_since_anchor_event)
            return balance_at_timestamp
        else:
            return 0

    
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

class ReceiptPrinter(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def connect_to_printer(self):
        self._client = escpos.printer.Network(
            self.ip_address
        )

    def print_deposit_receipt(self, account: Account) -> None:
        self._client.open()
        self._client.text("deposit receipt")

        self._client.cut()

    def print_withdrawal_receipt(self, account: Account) -> None:
        self._client.open()
        self._client.text("withdraw receipt")

        self._client.cut()


