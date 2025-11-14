import random
import datetime

def format_date_qualifier(date_format="D8", date_value=None):
    """
    Format a date with X12 date qualifier for DTP segments.

    Args:
        date_format (str): X12 date format qualifier code. Default: "D8" (CCYYMMDD format).
                          Common formats: D8 (date), RD8 (date range), TM (time)
        date_value (str, optional): Date value to format. If None, uses current date
                                   in YYYYMMDD format.

    Returns:
        str: Formatted date qualifier string in X12 format (e.g., "D8*20240430")

    Example:
        >>> format_date_qualifier("D8", "20240430")
        'D8*20240430'
        >>> format_date_qualifier()  # Uses today's date
        'D8*20250110'
    """
    date_value = date_value or datetime.datetime.now().strftime("%Y%m%d")
    return f"{date_format}*{date_value}"

def get_random_code(codes):
    """
    Select a random code from a list of medical codes.

    Args:
        codes (list): List of medical codes (ICD-10 or CPT-4 codes)

    Returns:
        str: Randomly selected code from the input list

    Example:
        >>> icd_codes = ['A00.0', 'A00.1', 'A00.9']
        >>> code = get_random_code(icd_codes)
        >>> code in icd_codes
        True
    """
    return random.choice(codes)
