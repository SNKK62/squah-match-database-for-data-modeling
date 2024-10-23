import unicodedata

def has_control_character(s: str) -> bool:
    return any(map(lambda c: unicodedata.category(c) == 'Cc', s))
