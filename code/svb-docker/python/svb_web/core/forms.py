from django import forms
from core.models import Customer, Account, NewsArticle, NewsAuthor

class CustomerLookupForm(forms.Form):
    customer_id = forms.CharField(max_length=Customer.CUSTOMER_ID_MAX_LENGTH)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def clean(self):
        """
        @brief Cleaning function automatically called on all CustomerForm fields. Used to call
        the get_new_customer_id function from models.py to get the next unused customer number.

        Note: Race condition avoided since default ID is set to "TBA". If multiple forms are
        submitted at the exact same instant, one will fail as they will collide with the "TBA"
        primary key.
        """
        cleaned_data = super().clean()
        if cleaned_data.get('customer_id') == "TBA":
            # New customer is being created.
            if not cleaned_data.get('first_name') or cleaned_data.get('customer'):
                # Return empty string as customer ID if something goes wrong to trigger a blank
                # field error.
                raise forms.ValidationError(
                    "Blank first name or costume not allowed!"
                )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author', 'preview', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']
