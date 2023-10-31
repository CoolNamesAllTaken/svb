from django import forms
from core.models import Customer, Account, NewsArticle, NewsAuthor
from django.core.exceptions import ObjectDoesNotExist # used in CustomerForm

class CustomerLookupForm(forms.Form):
    customer_id = forms.CharField(max_length=Customer.CUSTOMER_ID_MAX_LENGTH)

class CustomerForm(forms.ModelForm):
    referrer_str = forms.CharField(
        label="Referrer",
        max_length=Customer.CUSTOMER_ID_MAX_LENGTH, 
        required=False,
    )

    class Meta:
        model = Customer
        exclude = ['referrer']
    
    def clean(self):
        """
        @brief Cleaning function automatically called on all CustomerForm fields. Used to call
        the get_new_customer_id function from models.py to get the next unused customer number.

        Note: Race condition avoided since default ID is set to "TBA". If multiple forms are
        submitted at the exact same instant, one will fail as they will collide with the "TBA"
        primary key.
        """
        cleaned_data = super().clean()

        # Convert the referrer_str into a proper ForeignKey.
        referrer_str = cleaned_data.get('referrer_str')
        # cleaned_data['referrer'] = Customer.objects.get(pk=referrer_str)
        if referrer_str == "":
            cleaned_data['referrer'] = None
        else:
            try:
                cleaned_data['referrer'] = Customer.objects.get(pk=referrer_str)
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    f"Can't find referring Customer with customer_id {referrer_str}"
                )
        return cleaned_data

class AccountTransactionForm(forms.Form):
    customer_id = forms.CharField(
        max_length=Customer.CUSTOMER_ID_MAX_LENGTH,
        disabled=True
    )
    action = forms.ChoiceField(
        choices= [
            ("DEPOSIT", "Make a deposit."),
            ("WITHDRAW", "Make a withdrawal."),
            ("TRANSFER", "Transfer funds between accounts."),
            ("CLOSEOUT", "Withdraw all funds and close account.")
        ]
    )
    from_account = forms.ModelChoiceField(
        queryset=Account.objects.all(), # Overwrite this with initial value.
        required=False 
    )
    to_account = forms.ModelChoiceField(
        queryset=Account.objects.all(), # OVerwrite this with initial value.
        required=False # Not needed for closeouts or withdrawals.
    )
    amount = forms.IntegerField(
        min_value=0,
        required=False # Not needed for closeouts.
    )
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['from_account'] not in Account.objects.filter(customer__customer_id=cleaned_data['customer_id']):
            raise forms.ValidationError(
                f"From Account does not belong to customer with ID {cleaned_data['customer_id']}"
            )
        if cleaned_data['to_account'] not in Account.objects.filter(customer__customer_id=cleaned_data['customer_id']):
            raise forms.ValidationError(
                f"To Account does not belong to customer with ID {cleaned_data['customer_id']}"
            )
        # Don't bother returning cleaned_data, not overriding anything.
class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author', 'preview', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']


class InitializeBankForm(forms.Form):
    initial_bank_reserves = forms.IntegerField()


class FreezeRatesBankForm(forms.Form):
    pass


class UpdateRatesBankForm(forms.Form):
    new_interest_rate = forms.FloatField()


class SetEekLevelBankForm(forms.Form):
    new_eek_level = forms.IntegerField()


class MakeWithdrawalForm(forms.Form):
    withdrawal_amount = forms.IntegerField()
    account_number = forms.CharField()
    