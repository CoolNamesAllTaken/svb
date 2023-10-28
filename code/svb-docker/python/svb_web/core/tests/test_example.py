import pytest
import core.models as models

class TestExampleClass:
    TEST_CONSTANT = 1

    @pytest.mark.django_db
    def test_basic_pytest_django_models(self):
        customer = models.Customer(customer_id='1')
        customer.save()
        database_customer = models.Customer.objects.get(customer_id='1')

        assert database_customer.customer_id == customer.customer_id