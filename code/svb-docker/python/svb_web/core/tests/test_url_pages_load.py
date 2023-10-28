import pytest
from django.urls import reverse, get_resolver
from django.urls.exceptions import NoReverseMatch

class TestUrls:
    STATUS_CODES_OK = [200, 204, 302]

    def test_basic(self):
        assert 1

    @pytest.mark.django_db
    @pytest.mark.parametrize("url_lookup_name", 
                             [n for n in get_resolver().reverse_dict.keys() if isinstance(n, str)])
    def test_urls_return_status_ok(self, client, url_lookup_name):
        try:
            full_url = reverse(url_lookup_name)
        except NoReverseMatch:
            return
        else:
            response = client.get(full_url)
            assert response.status_code in self.STATUS_CODES_OK
