from modules import scripts

import os
import re


SAMPLE_FOLDER = os.path.join(scripts.basedir(), "samples")
CARDS_FOLDER = os.path.join(scripts.basedir(), "cards")
TAGS_FOLDER = os.path.join(scripts.basedir(), "tags")


def sanitize(item: str) -> str:
    """Convert an arbitrary string into a web-safe text for display"""
    return re.sub("[^a-zA-Z0-9 \.]", "", item).replace(" ", "_")


def sanitize_int(index: int) -> str:
    """Convert a number into string for sorting"""
    return f"{index:03}"
