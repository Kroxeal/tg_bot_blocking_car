import re


def validate_phone_number(phone_number):
    phone_number_pattern = r'^\+\d{3}\d{2}|\d{2}\d{7}$'
    return re.match(phone_number_pattern, phone_number) is not None
