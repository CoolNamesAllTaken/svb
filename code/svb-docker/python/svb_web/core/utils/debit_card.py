from django.shortcuts import get_object_or_404, get_list_or_404
from core.models import Customer

from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os # for file path stuff
import yaml # for config stuff

import qrcode

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
    