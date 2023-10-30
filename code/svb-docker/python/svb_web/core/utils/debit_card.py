from django.shortcuts import get_object_or_404, get_list_or_404
from core.models import Customer

from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os # for file path stuff
import yaml # for config stuff

import qrcode

def parse_customer_id_from_url(url):
    """
    @brief Parses a URL of type svb.pantsforbirds.com/c/<customer_id> and returns just the customer ID.
    @param[in] URL String to parse customer_id from.
    @retval Parsed customer ID, or None if it wasn't found.
    """
    tokenized_url = url.split('/')
    if tokenized_url[0] != "svb.pantsforbirds.com" or tokenized_url[1] != "c":
        return None
    else:
        return tokenized_url[2]

def generate_customer_qr_code(customer: Customer):
    pass

def create_debit_card(customer):
    pass

def assemble_debit_card(
    output_path="/app/media/customers/misc",
    save_pdf=True,
    first_name="Edween",
    costume="Founder",
    customer_id="EFYYMMDDNNNN"
):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    