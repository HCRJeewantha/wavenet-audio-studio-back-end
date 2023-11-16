import re


def email_validation(cls, value):
    if value == "":
        raise ValueError('email address required')

    pattern = "^[a-zA-Z0-9-._]+@[a-zA-Z0-9.]+\.[a-z]{1,3}$"
    if re.match(pattern, value):
        return value
    raise ValueError('Invalid email address')
