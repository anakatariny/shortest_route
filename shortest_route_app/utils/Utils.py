def is_number(possible_value):
    """
    this functions checks if the third value from a row is a number or can be converted in one
    :param possible_value: the value that will be tested, the validation is correct if the value is a float
    :return: boolean
    """
    try:
        float(possible_value)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(possible_value)
        return True
    except (TypeError, ValueError):
        pass
    return False