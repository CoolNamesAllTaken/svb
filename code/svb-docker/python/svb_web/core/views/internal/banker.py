from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from core.models import Customer
from django.contrib.auth.decorators import login_required
import os.path
from core.forms import CustomerForm, CustomerLookupForm
from core.utils.debit_card import encode_debit_card_image


@login_required
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


# @login_required
def create_customer_from_form(form):
    """
    @brief Helper function that allows creation of a Customer object from a CustomerForm.
    @retval Customer that was created (with generated customer_id).
    """
    if form.is_valid():
        # Manually override the customer fields with cleaned fields since calling form.is_valid() and form.save() on their own
        # does not actually save the form with cleaned data, just with raw data.
        cleaned_data = form.clean()
        customer, created = Customer.objects.get_or_create(pk=cleaned_data['customer_id'])
        customer.first_name = cleaned_data['first_name']
        customer.costume = cleaned_data['costume']
        customer.referrer = cleaned_data['referrer']
        customer.joined_date = cleaned_data['joined_date']
        customer.security_candy = cleaned_data['security_candy']
        customer.save() # Caitlin loves John a lot <3
        # Update the Customer model in the database with new info.

    return customer


@login_required
def edit_customer(request, customer_id=None):
    """
    @brief View function that allows editing of a Customer via a form submission.
    """
    if customer_id:
        # Editing an existing customer.
        customer = get_object_or_404(Customer, pk=customer_id)
        form_title = "Edit Existing Customer"
        submit_button_label = "Update"
        debit_card_rear_image = encode_debit_card_image(customer.get_debit_card_path(pdf=False))
    else:
        # Creating a new customer.
        customer=None
        form_title = "Create New Customer"
        submit_button_label = "Create"
        debit_card_rear_image = encode_debit_card_image(os.path.join(settings.STATIC_ROOT, "core", "debit_card", "svb_debit_card_rear_blank.png"))

    if request.method == 'POST':
        # POST = submitting a form to update customer info.
        # Create a form instance and populate it with data from the request (binding).
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        # Not for human consumption, since the only way the user sees this form is if the form is not valid even though it was POSTed.
        # Disable the sensitive fields anyways, just to be safe.
        form.fields['customer_id'].disabled = True
        
        # Check if the form is valid.
        if form.is_valid():
            # Process the data in form.cleaned_data as required.
            customer = create_customer_from_form(form)

            # Redirect to a new URL:
            return HttpResponseRedirect('/internal/customer/edit/' + customer.customer_id)
       
    else:
        # GET (or other) = default form for creating a new customer.
        if customer:
            referrer_str_initial = customer.referrer
        else:
            referrer_str_initial = ""
        form = CustomerForm(
            instance=customer, 
            initial={'referrer_str': referrer_str_initial}
        )
        form.fields['customer_id'].disabled = True

    context = {
        'form': form,
        'form_title': form_title,
        'submit_button_label': submit_button_label,
        'customer_id': customer_id,
        'debit_card_front_image': encode_debit_card_image(os.path.join(settings.STATIC_ROOT, "core", "debit_card", "svb_debit_card_front.png")),
        'debit_card_rear_image': debit_card_rear_image
    }
    return render(request, "internal/edit_customer.html", context)


@login_required
def lookup_account(request):
    context = {}
    return render(request, "internal/lookup_account.html", context)


@login_required
def edit_account(request):
    context = {}
    return render(request, "internal/edit_account.html", context)