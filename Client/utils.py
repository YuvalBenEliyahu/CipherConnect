def get_input(prompt, validation_func, error_message):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(error_message)


def validate_non_empty(value):
    return bool(value)


def validate_phone_number(value):
    return value.isdigit() and len(value) == 10 and value.startswith("05")