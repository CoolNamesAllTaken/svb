from datetime import datetime, timezone

DATETIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S.%f %Z"

def get_current_utc_timestamp():
    """
    @brief Function to get the current timezone aware timestamp.
    """
    return datetime.now(tz=timezone.utc)

def get_current_utc_timestamp_str():
    """
    @brief Returns a properly formatted datetime string that can be re-ingested.
    Good for form fields.
    """
    return datetime.now(tz=timezone.utc).strftime(DATETIME_STR_FORMAT)

def get_timestamp_from_utc_str(utc_str):
    return datetime.strptime(utc_str, DATETIME_STR_FORMAT)