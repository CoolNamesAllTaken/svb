from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from core.models import Customer

from core.forms import CustomerForm, CustomerLookupForm
from core.utils.debit_card import *

def lookup_customer(request, customer_id=None):
    """
    @brief View function that allows looking up of a Customer via a form submisison.
    @param[in] customer_id ID of a customer from a previous failed lookup. Correct lookups
        should result in a redirect, so we don't expect them to go back to this view
        function.
    """
    message = "Lookup customer by ID."
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CustomerLookupForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            customer_id = form.cleaned_data['customer_id']
            try:
                customer = get_object_or_404(Customer, pk=customer_id)
                # redirect to a new URL:
                return HttpResponseRedirect('/internal/customer/edit/' + customer_id + '/')
            except:
                message = "Customer ID {} not found!".format(customer_id)
        else:
            message = "Form contents not valid. Try again!"
    else:
        form = CustomerLookupForm()
    
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, "internal/lookup_customer.html", context)


def create_customer_from_form(form):
    """
    @brief Helper function that allows creation of a Customer object from a CustomerForm.
    """
    form.save() # Update the Customer model in the database with new info.

    # TODO: Build and save debit card.
    customer = get_object_or_404(Customer, pk=form.cleaned_data['customer_id'])
    create_debit_card(customer)



def edit_customer(request, customer_id=None):
    """
    @brief View function that allows editing of a Customer via a form submission.
    """
    print(f"edit_customer with customer_id={customer_id}")
    if customer_id:
        # Editing an existing customer.
        customer = get_object_or_404(Customer, pk=customer_id)
        form_title = "Edit Existing Customer"
        submit_button_label = "Update"
    else:
        # Creating a new customer.
        customer=None
        form_title = "Create New Customer"
        submit_button_label = "Create"
    if request.method == 'POST':
        # POST = submitting a form to update customer info.
        # Creat a form instance and populate it with data from the request (binding).
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        # Not for human consumption, since the only way the user sees this form is if the form is not valid even though it was POSTed.
        # Disable the sensitive fields anyways, just to be safe.
        form.fields['customer_id'].disabled = True

        # Check if the form is valid.
        if form.is_valid():
            # Process the data in form.cleaned_data as required.
            create_customer_from_form(form)

            # Redirect to a new URL:
            return HttpResponseRedirect('/internal/customer/edit/' + form.cleaned_data['customer_id'])
    else:
        # GET (or other) = default form for creating a new customer.
        form = CustomerForm(instance=customer)
        form.fields['customer_id'].disabled = True

    if customer_id:
        # Customer already exists, enable print function and maybe other things.
        pass
    else:
        pass

    context = {
        'form': form,
        'form_title': form_title,
        'submit_button_label': submit_button_label,
        'customer_id': customer_id,
    }
    return render(request, "internal/edit_customer.html", context)

def lookup_account(request):
    context = {}
    return render(request, "internal/lookup_account.html", context)

def edit_account(request):
    context = {}
    return render(request, "internal/edit_account.html", context)