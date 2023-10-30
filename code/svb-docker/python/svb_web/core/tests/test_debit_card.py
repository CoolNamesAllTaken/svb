import pytest
import core.models as models

import core.utils.debit_card as debit_card_utils

def test_parse_customer_id_from_url():
    assert debit_card_utils.parse_customer_id_from_url("svb.pantsforbirds.com/c/potatoes") == "potatoes"
    assert debit_card_utils.parse_customer_id_from_url("hello/potatoes") == None
    assert debit_card_utils.parse_customer_id_from_url("https://svb.pantsforbirds.com/c/doot") == "doot"
    assert debit_card_utils.parse_customer_id_from_url("http://svb.pantsforbirds.com/c/poton") == "poton"
    assert debit_card_utils.parse_customer_id_from_url("http://svb.pantsforbirds.com/c/potdon/after") == "potdon"