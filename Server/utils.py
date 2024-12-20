import re


def password_check(passwd):
    # Check if password length is between 6 and 20 characters
    if (6 <= len(passwd) <= 20 and
            # Check if password contains at least one digit
            re.search(r'\d', passwd) and
            # Check if password contains at least one uppercase letter
            re.search(r'[A-Z]', passwd) and
            # Check if password contains at least one lowercase letter
            re.search(r'[a-z]', passwd) and
            # Check if password contains at least one special symbol
            re.search(r'[$@#%!&*^?:;,./<>|~`+\-=_{}[\]()]', passwd)):
        return True
    return False


