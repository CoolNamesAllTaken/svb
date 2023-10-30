# Core Views
This folder contains the render function for all of the views used by the `core` app.

## How to add a new view
1. Add file to the relevant `views/<subfolder>` directory.
2. Add an import to `views/__init__.py` to gather the relevant render functions into the `views` module accessible from the rest of the python project.
3. If render function names or paths have been updated, resolve issues in `urls.py`, both in the `core` app and in the top level Django project.

## Folders and Files
* `internal` - Specialized views for employees and internal use.
    * `author.py` - Render functions used for authors who write articles for the website.
    * `banker.py` - Render functions used by bankers.
    * `common.py` - Render functions that are reused everywhere for internal users.
    * `display.py` - Render functions used for internal displays inside SVB.
* `public` - Views that are publicly available without login.
    * `common.py`- Render functions that are reused everywhere for internal users.
    * `customer.py` - Render functions used by customers when viewing their account.
    * `visitor.py` - Render functions used by casual visitors to the website (don't need to be customers).