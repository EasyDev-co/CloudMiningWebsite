import re


PHONE_NUMBER_PATTERN = re.compile(r"^[1-9][0-9]{7,14}$")