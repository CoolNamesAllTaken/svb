from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os # for file path stuff

from datetime import date

import base64 # for encoding debit card images
import qrcode

# ID card dimensions: 86x54mm
# Zebra P330i resolution: 300dpi, recommended resolution 600dpi+
DEBIT_CARD_DPI = 600
DEBIT_CARD_GLOBAL_X_OFFSET_MM = 1
MM_PER_IN = 25.4
PT_PER_IN = 72
DEBIT_CARD_WIDTH_MM = 86
DEBIT_CARD_HEIGHT_MM = 54
STANDARD_PADDING = 4
TEXT_PADDING = 4
STRIPE_BOTTOM_Y = 12.5
QR_CODE_TOP_LEFT = (STANDARD_PADDING, STANDARD_PADDING + STRIPE_BOTTOM_Y)
QR_CODE_SIDE_LENGTH_MM = 26
CANDY_BAR_HEIGHT = 24
DEBIT_CARD_TEXT_HEIGHT_PT = 6

DEBIT_CARD_TEMPLATE_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "static", "core", "debit_card", "svb_debit_card_rear_blank.png")
CANDY_BAR_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "static", "core", "debit_card", "svb_logo_silhouette.png")
DEBIT_CARD_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "static", "core", "debit_card", "Arial.ttf")
DEBIT_CARD_BOLD_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "static", "core", "debit_card", "Arial_Bold.ttf")

def parse_customer_id_from_url(url: str):
    """
    @brief Parses a URL of type svb.pantsforbirds.com/c/<customer_id> and returns just the customer ID.
    @param[in] URL String to parse customer_id from.
    @retval Parsed customer ID, or None if it wasn't found.
    """
    customer_domain = f"{settings.ROOT_DOMAIN}/c/"
    domain_beginning = url.rfind(customer_domain)
    if domain_beginning == -1:
        return None # Domain beginning wasn't found.
    url = url[domain_beginning+len(customer_domain):]
    tokenized_url = url.split('/')
    return tokenized_url[0] # just return the customer in case there's stuff afterwards

"""Public Functions"""

def assemble_debit_card_image(
    output_path,
    save_pdf=True,
    first_name="Edween",
    costume="Founder",
    customer_id="EFYYMMDDNNNN",
    customer_page_url="svb.pantsforbirds.com",
    joined_date=date.today()
):
    """
    @brief Builds and ID card PNG and optional PDF file from text fields and image files.
    @param[in] output_path Full path of output image with desired extension (.png).
    @param[in] save_pdf Optional parameter, also saves a PDF if set to True.
    @param[in] first_name First name to display on debit card.
    @param[in] costume Costume name to display on debit card.
    @param[in] customer_id Customer ID to display on debit card.
    @param[in] customer_page_url URL to encode into the QR code and embed in the debit card.
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print("Assembling debit card at {}.".format(output_path))

    # Set up for putting text onto ID card
    debit_card = Image.open(DEBIT_CARD_TEMPLATE_IMAGE_PATH)
    debit_card = debit_card.resize((mm2pix(DEBIT_CARD_WIDTH_MM), mm2pix(DEBIT_CARD_HEIGHT_MM))) #TODO: find out if this is necessary

    qr_code_image = qrcode.make(customer_page_url, border = 0)
    qr_code_image = qr_code_image.resize((mm2pix(QR_CODE_SIDE_LENGTH_MM), mm2pix(QR_CODE_SIDE_LENGTH_MM)))
    debit_card.paste(qr_code_image, (mm2pix(QR_CODE_TOP_LEFT[0]), mm2pix(QR_CODE_TOP_LEFT[1])))

    candy_bar_image = Image.open(CANDY_BAR_IMAGE_PATH)
    CANDY_BAR_WIDTH = pix2mm(candy_bar_image.width * mm2pix(CANDY_BAR_HEIGHT) / candy_bar_image.height)
    candy_bar_image = candy_bar_image.resize((mm2pix(CANDY_BAR_WIDTH), mm2pix(CANDY_BAR_HEIGHT)))
    debit_card.paste(candy_bar_image, (mm2pix(DEBIT_CARD_WIDTH_MM - STANDARD_PADDING - CANDY_BAR_WIDTH), mm2pix(DEBIT_CARD_HEIGHT_MM - STANDARD_PADDING - CANDY_BAR_HEIGHT)))

    debit_card_canvas = ImageDraw.Draw(debit_card)
    debit_card_fontsize_pix = math.ceil(DEBIT_CARD_TEXT_HEIGHT_PT / PT_PER_IN * DEBIT_CARD_DPI)
    
    # debit_card_font_smaller = ImageFont.truetype(DEBIT_CARD_FONT_PATH, int(0.8*debit_card_fontsize_pix))
    # debit_card_font_small = ImageFont.truetype(DEBIT_CARD_FONT_PATH, debit_card_fontsize_pix) # Bold 6pt Arial font
    debit_card_font_medium = ImageFont.truetype(DEBIT_CARD_FONT_PATH, int(1.3*debit_card_fontsize_pix))
    debit_card_font_medium_bold = ImageFont.truetype(DEBIT_CARD_BOLD_FONT_PATH, int(1.3*debit_card_fontsize_pix))
    debit_card_font_large = ImageFont.truetype(DEBIT_CARD_FONT_PATH, int(1.7*debit_card_fontsize_pix))
    debit_card_font_large_bold = ImageFont.truetype(DEBIT_CARD_BOLD_FONT_PATH, int(1.7*debit_card_fontsize_pix))
    
    text_origin = (mm2pix(2 * STANDARD_PADDING + QR_CODE_SIDE_LENGTH_MM), mm2pix(STRIPE_BOTTOM_Y + STANDARD_PADDING + 2.5))
    debit_card_canvas.text(text_origin, (first_name + " " + costume).upper(), font=debit_card_font_large_bold, fill=(0, 0, 0), anchor='ls')
    
    text_origin = (text_origin[0], text_origin[1] + mm2pix(TEXT_PADDING))
    debit_card_canvas.text(text_origin, "Customer ID: ", font=debit_card_font_medium, fill=(0, 0, 0), anchor='ls')
    temp = (text_origin[0] + 396, text_origin[1])
    debit_card_canvas.text(temp, customer_id, font=debit_card_font_medium_bold, fill=(0, 0, 0), anchor='ls')
    
    text_origin = (text_origin[0], text_origin[1] + mm2pix(TEXT_PADDING))
    debit_card_canvas.text(text_origin, "Member Since: ", font=debit_card_font_medium, fill=(0, 0, 0), anchor='ls')
    temp = (text_origin[0] + 450, text_origin[1])
    debit_card_canvas.text(temp, str(joined_date), font=debit_card_font_medium, fill=(0, 0, 0), anchor='ls')
    
    text_origin = (text_origin[0], text_origin[1] + mm2pix(3 * TEXT_PADDING))
    debit_card_canvas.text(text_origin, "Silicandy Valley Bank", font=debit_card_font_large, fill=(0, 0, 0), anchor='ls')

    bottom_text_origin = (mm2pix(STANDARD_PADDING), mm2pix(STRIPE_BOTTOM_Y + 2 * STANDARD_PADDING + QR_CODE_SIDE_LENGTH_MM))
    debit_card_canvas.text(bottom_text_origin, "Scan the QR code above or view your accounts at:", font=debit_card_font_medium, fill=(0, 0, 0), anchor='ls')
    bottom_text_origin = (bottom_text_origin[0], bottom_text_origin[1] + mm2pix(TEXT_PADDING))
    debit_card_canvas.text(bottom_text_origin, customer_page_url, font=debit_card_font_medium_bold, fill=(0, 0, 0), anchor='ls')

    debit_card.save(output_path)
    if save_pdf:
        debit_card.save(os.path.splitext(output_path)[0] + ".pdf")

def encode_debit_card_image(image_path):
    """
    @brief Returns a base64 encloded string of an image at a given path, or the blank ID card image if the image is not found.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    except:
        with open(DEBIT_CARD_TEMPLATE_IMAGE_PATH, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data
    


"""Private Utility Functions"""

def pix2mm(pix):
    return pix/DEBIT_CARD_DPI*MM_PER_IN

def mm2pix(mm):
    return int(mm/MM_PER_IN*DEBIT_CARD_DPI)