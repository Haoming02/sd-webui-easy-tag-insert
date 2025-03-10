import re

special = re.compile("[^\w\s]")


def sanitize(item: str) -> str:
    """Convert an arbitrary string into a web-safe text for display"""
    return re.sub(special, "", item).replace(" ", "-")


def sanitize_int(index: int) -> str:
    """Convert a number into string for sorting"""
    return f"{index:03}"
