import re


def validate_license_plate(license_plate):
    license_plate_pattern = r'^\d{4}\s[A-Z]{2}-[1-7]$'
    return re.match(license_plate_pattern, license_plate) is not None
