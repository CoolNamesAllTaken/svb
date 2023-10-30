from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from core.models import Customer
from django.contrib.auth.decorators import login_required
from core.forms import CustomerLookupForm

def lookup_accounts(request, customer_id=None):
    """
    @brief View function that allows looking up a Customer's accounts using their customer ID.
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
                return HttpResponseRedirect('/internal/accounts/edit/' + customer_id + '/')
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
    
    return render(request, "internal/lookup_accounts.html", context)