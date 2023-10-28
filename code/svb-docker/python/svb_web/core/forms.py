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


class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author', 'preview', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']
