from django import forms
from core.models import Customer, Account, NewsArticle, NewsAuthor, get_new_customer_id

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def clean_customer_id(self):
        """
        @brief Cleaning function automatically called on the customer_id form field. Used to call
        the get_new_customer_id function from models.py to get the next unused customer number.

        Note: Race condition avoided since default field is set to "TBA". If multiple forms are
        submitted at the exact same instant, one will fail as they will collide with the "TBA"
        primary key.
        """
        if self.cleaned_data.get('customer_id') == "TBA":
            return get_new_customer_id()
        return self.cleaned_data.get('customer_id')


class ArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['headline', 'author', 'preview', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = NewsAuthor
        fields = ['name', 'title']
