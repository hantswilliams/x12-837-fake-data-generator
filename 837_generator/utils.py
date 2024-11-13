import random
import datetime

def format_date_qualifier(date_format="D8", date_value=None):
    date_value = date_value or datetime.datetime.now().strftime("%Y%m%d")
    return f"{date_format}*{date_value}"

def get_random_code(codes):
    return random.choice(codes)
