## Directories
* `simulation` - Files for simulating interest rates etc.
* `svb-docker` - Docker project that runs the web server.
* `id_card_printer` - Python scripts for running the ID card printer on a windows machine (connected via USB).

## Run the Thing!
1. Start the webserver by running `docker compose up` from the `svb-docker` directory.
2. Start the ID card print server by running `poetry run print_server.py` from the `print_server` directory.