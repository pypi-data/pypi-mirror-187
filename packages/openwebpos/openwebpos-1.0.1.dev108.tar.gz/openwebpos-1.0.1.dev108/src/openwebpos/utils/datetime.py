from datetime import date, datetime


def get_ymd_date() -> str:
    """
    Get the current date in YMD format

    Returns:
         The current date in YMD format
    """
    now = datetime.now()
    return now.strftime("%y%m%d")


def get_hms_time() -> str:
    """
    Get the current time in HM format

    Returns:
         The current time in HM format
    """
    now = datetime.now()
    return now.strftime("%H%M%S")


def get_current_date() -> date:
    """
    Get the current date

    Returns:
         The current date
    """
    return date.today()
