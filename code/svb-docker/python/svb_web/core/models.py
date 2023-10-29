from __future__ import annotations # allow type hinting with the type of the enclosing class

from django.db import models
from datetime import date, datetime, timezone
import escpos.printer
import math

def get_utc_timestamp():
    """
    @brief Function to get the current timezone aware timestamp.
    """
    return datetime.now(tz=timezone.utc)


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
    
    def get_absolute_url(self):
        return f"c/{self.customer_id}"

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
    ACCOUNT_NAME_MAX_LENGTH = 80 # maximum number of characters for the account name

    account_number = models.AutoField(primary_key=True)
    account_name = models.CharField(default="", max_length=ACCOUNT_NAME_MAX_LENGTH)
    customer = models.ForeignKey(
        "Customer",
        # Don't allow blank since forms creating an account must specify a customer.
        null=True, # allow NULL values in storage
        on_delete=models.CASCADE # delete Account when associated Customer is deleted
    )

    # Account balance at current timestamp can be calculated from previous anchor event
    # timestamp and anchor event account balance.
    def get_balance(self, timestamp=None):
        """
        @brief Returns the balance of the account at the given timestamp. Backdates to the last anchor event.
        And calculates the interest accrued since then.
        @param[in] timestamp Datetime timestamp to calculate interest at.
        @retval Account balance at the specified timestamp. Uses current timestamp if not specified.
        """
        COMPOUNDING_INTERVAL_SECONDS = 1800
        if timestamp is None:
            timestamp = get_utc_timestamp()
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

    def get_last_anchor_event(self, timestamp=None):
        """
        @brief Helper function that returns the last AnchorEvent, or the last anchor event that occurred before an optional timestamp. Used
        by the other getter functions.
        @param[in] timestamp Optiona ltimestamp to find the most recent anchor event before.
        @retval The most recent AnchorEvent, or None if the account has not been initialized.
        """
        if timestamp is None:
            timestamp = get_utc_timestamp()
        most_recent_anchor_events = AnchorEvent.objects.filter(account__exact=self, timestamp__lte=timestamp)
        if len(most_recent_anchor_events) == 0:
            return None
        return most_recent_anchor_events.latest('timestamp')
    
    def get_interest_rate(self, timestamp=None):
        """
        @brief Returns the current interest rate of an account, or the most recent interest rate before a specified timestamp.
        @param[in] timestamp Optional timestamp to find the most recent interest rate before.
        """
        if timestamp is None:
            timestamp = get_utc_timestamp()
        last_anchor_event = self.get_last_anchor_event(timestamp=timestamp)
        if last_anchor_event is None:
            raise RuntimeError(f"Attempted to get interest rate from account {self.account_number} ({self.account_name}) before it was initialized.")
        return last_anchor_event.interest_rate
    
    def set_interest_rate(self, interest_rate, timestamp=None):
        """
        @brief Sets the interest rate of the account, with an optional specified timestamp that must be in the past and more recent
        than the most recent anchor event.
        @param[in] interest_rate New interest rate to set.
        @param[in] timestamp Optional timestamp in the past (must be newer than most recent AnchorEvent) to set the interest at.
        """
        if timestamp is None:
            timestamp = get_utc_timestamp()
        last_anchor_event = self.get_last_anchor_event(timestamp=timestamp)
        if last_anchor_event is None:
            raise RuntimeError(f"Attempted to set interest rate for account {self.account_number} ({self.account_name}) before it was initialized.")
        if last_anchor_event.timestamp > timestamp: # Note: this is a deliberate >, not >=. Timestamp resolution is ~100ms.
            raise RuntimeError(f"Attempted to set interest rate for account {self.account_number} ({self.account_name}) before the most recent AnchorEvent.")
        anchor_event = AnchorEvent(
            account=self,
            category=AnchorEvent.UPDATE_INTEREST,
            timestamp=timestamp,
            balance=self.get_balance(timestamp),
            interest_rate=interest_rate
        )
        anchor_event.save()
        # Handle special case where two anchor events occur too close together and timestamp resolution isn't sufficient: overwrite previous
        # anchor event with the new one.
        if last_anchor_event.timestamp == anchor_event.timestamp:
            last_anchor_event.delete()

    def init(
            self,
            timestamp=None,
            balance=0.0,
            interest_rate=0.0
    ):
        """
        @brief Creates an initialization anchor event for an account.
        @param[in] init_timestamp Timestamp for ACCOUNT_CREATED AnchorEvent. Must be in the past.
        @param[in] init_balance Starting account balance (defaults to 0).
        @param[in] init_interest_rate Initial interest rate for the account, over the set compounding interval.
        @retval The initialization AnchorEvent.
        """
        if timestamp is None:
            timestamp = get_utc_timestamp()
        if AnchorEvent.objects.filter(account__exact=self):
            raise RuntimeError(f"Attemped to initalize account {self.account_number} ({self.account_name}) when it had pre-existing anchor events")
        if timestamp > datetime.now(tz=timezone.utc):
            raise ValueError(f"Cannot initialize an account with an AnchorEvent in the future.")

        init_anchor_event = AnchorEvent(
            account=self,
            category=AnchorEvent.ACCOUNT_CREATED,
            timestamp=timestamp,
            balance=balance,
            interest_rate=interest_rate
        )
        init_anchor_event.save()
        return init_anchor_event

    @classmethod
    def transfer_funds(
        cls,
        from_account: Account,
        to_account: Account, 
        amount: float
    ):
        """
        @brief Transfer funds from one account to another. Static method since it invokes on two accounts simultaneously.
        @param[in] from_account Account object to transfer funds out of.
        @param[in] to_account Account object to transfer funds into.
        @param[in] amount Amount to transfer.
        @retval True if success, False if failed.
        """
        last_from_account_anchor = from_account.get_last_anchor_event()
        last_to_account_anchor = to_account.get_last_anchor_event()
        if last_from_account_anchor is None or last_to_account_anchor is None:
            raise RuntimeError(f"Attempted a transfer between one or more accounts that weren't initialized.")

        # Create simulataneous deposit and withdrawal anchor events.
        transfer_timestamp = datetime.now(tz=timezone.utc)
        # Create withdrawal anchor event.
        withdrawal_anchor = AnchorEvent(
            account=from_account,
            category=AnchorEvent.WITHDRAWAL,
            timestamp=transfer_timestamp,
            balance=from_account.get_balance(timestamp=transfer_timestamp)-amount,
            # Don't think about the problem case of making a transfer before the most recent AnchorEvent.
            interest_rate=from_account.get_last_anchor_event().interest_rate
        )
        if withdrawal_anchor.balance < 0:
            print(
                f"Account transfer of f{amount} treats between account"
                f"{from_account.account_number} ({from_account.account_name}) ->"
                f"{to_account.account_number} ({to_account.account_name})"
                "failed due to insufficinet funds."
            )
            return False # abort the transfer due to insufficient funds
        # Create deposit anchor event.
        deposit_anchor = AnchorEvent(
            account=to_account,
            category=AnchorEvent.DEPOSIT,
            timestamp=transfer_timestamp,
            balance=to_account.get_balance(timestamp=transfer_timestamp)+amount,
            # Don't think about the problem case of making a transfer before the most recent AnchorEvent.
            interest_rate=to_account.get_last_anchor_event().interest_rate
        )
        # Update anchor events and overwrite conflicting events (timestamp too close).
        if last_from_account_anchor.timestamp == withdrawal_anchor.timestamp:
            last_from_account_anchor.delete() # overwrite with new anchor
        withdrawal_anchor.save()
        if last_to_account_anchor.timestamp == deposit_anchor.timestamp:
            last_to_account_anchor.delete()
        deposit_anchor.save()
        return True
    
class AnchorEvent(models.Model):
    # Anchor Events:
    # - Account created.
    # - Interest rate changed.
    # - Candy deposited into account.
    # - Candy withdrawn from account.
    CATEGORY_NAME_MAX_LENGTH = 20

    ACCOUNT_CREATED = "UPDATE_INTEREST"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    UPDATE_INTEREST = "UPDATE_INTEREST"
    CATEGORY_CHOICES = [
        (ACCOUNT_CREATED, "Create the account."),
        (DEPOSIT, "Deposit funds into the associated account."),
        (WITHDRAWAL, "Withdraw funds from the associated account."),
        (UPDATE_INTEREST, "Update the interest rate of the associated account.")
    ]

    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE # delete AnchorEvent when its referenced Account is deleted.
    )
    category = models.CharField(
        max_length=CATEGORY_NAME_MAX_LENGTH,
        choices=CATEGORY_CHOICES,
        default=None
    )
    timestamp = models.DateTimeField(default=datetime.now) # Pass handle to datetime.now so it gets evaluated when the model is created, not defined!
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
        return self.date_published is not None and datetime.datetime.now(tz=timezone.utc) > self.date_published

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


