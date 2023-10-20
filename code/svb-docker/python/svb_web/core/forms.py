from django import forms
from core.models import Customer, Account, NewsArticle, NewsAuthor, get_new_customer_id

class CustomerLookupForm(forms.Form):
    customer_id = forms.CharField(max_length=Customer.kCustomerIdMaxLength)

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
            if not cleaned_data.get('first_name') or cleaned_data.get('customer'):
                # Return empty string as customer ID if something goes wrong to trigger a blank
                # field error.
                raise forms.ValidationError(
                    "Blank first name or costume not allowed!"
                )
            self.cleaned_data['customer_id'] = get_new_customer_id(
                cleaned_data.get('first_name'),
                cleaned_data.get('costume')
            )
            # except:
            #     # Return empty string as customer ID if something goes wrong to trigger a blank
            #     # field error.
            #     raise forms.ValidationError(
            #         "Blank first name or costume not allowed!"
            #     )
        # return cleaned_data.get('customer_id')


class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author', 'preview', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']
