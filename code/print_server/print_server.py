import win32api
import win32print

import os # for file path stuff
import yaml # for config stuff

PRINTER_ENUM_LEVEL = 2 # list printers on another server

def print_id_card(id_card_pdf_path):
    """
    @brief Prints an ID card given a path to a PDF file.
    """
    print("Printing ID Card: {}".format(id_card_pdf_path))
    win32api.ShellExecute(0, "print", id_card_pdf_path, None,  ".",  0)

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
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "id_card_config.yaml")) as f:
        config_dict = yaml.safe_load(f)
        # print(config_dict)

# NOTE: This script requires a PDF reader with shell extensions (like Foxit) to be installed and set as the default PDF reader!
def main():
    read_config()
    set_default_printer()
    id_card_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "outputs")
    assemble_id_card_image("{}/test.png".format(id_card_dir))
    print(encode_image(id_card_dir + "/test.png"))
    

    # print_id_card(os.path.join(id_card_dir, "test.pdf"))



if __name__ == "__main__":
    main()