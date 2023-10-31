import win32api
import win32print

import os # for file path stuff
from dotenv import load_dotenv
import yaml # for config stuff
import psycopg2

import time # for unix timestamp
MICROSECONDS_PER_SECOND = 1e6
PRINT_FILE_LIFETIME_S = 30

PRINTER_ENUM_LEVEL = 2 # list printers on another server
ENV_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "svb-docker", ".env.svb")
load_dotenv(ENV_FILE_PATH)

def print_debit_card(debit_card_pdf_path):
    """
    @brief Prints an ID card given a path to a PDF file.
    """
    print("Printing ID Card: {}".format(debit_card_pdf_path))
    win32api.ShellExecute(0, "print", debit_card_pdf_path, None,  ".",  0)

def initialize_id_printer():
    read_config()
    set_default_printer()

def set_default_printer():
    # First, try setting default printer to match the name provided in the config file.
    all_printers = [printer[2] for printer in win32print.EnumPrinters(PRINTER_ENUM_LEVEL)]
    for printer_num, printer in enumerate(all_printers):
        if printer == config_dict["printer"]:
            print("Found printer name from config file, setting default printer to {}.".format(printer))
            win32print.SetDefaultPrinter(all_printers[printer_num])
            return
            
    # Ask the user to select a printer
    printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
    # set the default printer
    win32print.SetDefaultPrinter(all_printers[printer_num])
    print("Manually set default printer to {}.".format(all_printers[printer_num]))

def read_config():
    global config_dict
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")) as f:
        config_dict = yaml.safe_load(f)
        # print(config_dict)

def get_timestamp_us():
    return int(time.time() * MICROSECONDS_PER_SECOND)

# NOTE: This script requires a PDF reader with shell extensions (like Foxit) to be installed and set as the default PDF reader!
def main():
    read_config()
    set_default_printer()
    debit_card_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "outputs")
    os.makedirs(debit_card_dir, exist_ok=True) # Make the output directory if it doesn't exist.

    connection = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'), 
        host="localhost", # must be on same machine as web server! 
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'), 
        password=os.getenv('POSTGRES_PASSWORD')
    )
    
    # get cursor
    cursor = connection.cursor()
    debit_card_print_jobs_query = "SELECT "
    while True:
        # Check for old files to delete.
        for file in os.listdir(debit_card_dir):
            if not file.endswith(".pdf"):
                continue # not interested
            file_timestamp = os.path.basename(file).split('.')[0]
            if not file_timestamp.isdigit():
                continue # didn't actually find a timestamp
            if int(file_timestamp) < (get_timestamp_us() - (PRINT_FILE_LIFETIME_S * MICROSECONDS_PER_SECOND)):
                os.remove(os.path.join(debit_card_dir, file))

        # Pull PDF binary data from the database
        get_latest_pdf_data_query = "select * from core_debitcardprintjob order by job_number asc;"
        cursor.execute(get_latest_pdf_data_query)
        job_data = cursor.fetchone()

        if job_data is None:
            continue # busy wait

        job_number = job_data[0]
        timestamp = job_data[1]
        job_pdf_bytes = job_data[2]
    
        print(f"Printing Debit Card: job_number={job_number} timestamp={timestamp} num_bytes={len(job_pdf_bytes)}")

        # Dump binary data to a file and print.
        pdf_filepath = os.path.join(debit_card_dir, f"{get_timestamp_us()}.pdf")
        with open(pdf_filepath, 'wb') as file:
            file.write(job_pdf_bytes)
        print_debit_card(pdf_filepath)
        delete_latest_print_job_query = f"delete from core_debitcardprintjob where job_number = {job_number};"
        cursor.execute(delete_latest_print_job_query)
        connection.commit()

if __name__ == "__main__":
    main()