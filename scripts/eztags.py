from modules.ui_extra_networks import ExtraNetworksPage, quote_js, register_page
from modules import shared, script_callbacks

from scripts.ez_utils import (
    SAMPLE_FOLDER,
    CARDS_FOLDER,
    TAGS_FOLDER,
    sanitize,
    sanitize_int,
)

import shutil
import glob
import os


class EasyTags(ExtraNetworksPage):

    def __init__(self):
        super().__init__("EZ Tags")
        self.allow_negative_prompt = True
        self.cards: list[str] = None

        if os.path.exists(TAGS_FOLDER):
            print('\n[EZ Tags] "tags" folder has been deprecated. You may delete it~\n')
        if not os.path.exists(CARDS_FOLDER):
            print('\n[EZ Tags] "cards" folder not found. Initializing...\n')
            shutil.copytree(SAMPLE_FOLDER, CARDS_FOLDER)

        self.refresh()

    def refresh(self):
        self.cards = []
        objs = glob.glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)

        for obj in objs:
            if os.path.isdir(obj):
                continue

            if obj.endswith(".tag"):
                self.cards.append(obj)
            else:
                print(f'[EZ Tags] Invalid File: "{obj}"')

    def create_item(self, filename: str, i: str):
        with open(filename, "r", encoding="utf-8") as card:
            prompt = card.read().strip()

        path, ext = os.path.splitext(filename)
        relative_path = os.path.relpath(path, CARDS_FOLDER)

        category, name = relative_path.rsplit(os.sep, 1)

        return {
            "name": name.strip(),
            "filename": filename,
            "shorthash": f"{hash(filename)}",
            "preview": None,
            "description": None,
            "search_terms": [self.search_terms_from_path(filename)],
            "prompt": quote_js(prompt),
            "local_preview": f"{path}.preview.{shared.opts.samples_format}",
            "sort_keys": {
                "default": sanitize(f"{category.lower()}-{name.lower()}"),
                "date_created": i,
                "date_modified": sanitize(f"{category.lower()}-{i}"),
                "name": sanitize(name.lower()),
            },
        }

    def list_items(self):
        i = 0

        for FILE in self.cards:
            i += 1
            yield self.create_item(FILE, sanitize_int(i))

    def allowed_directories_for_previews(self):
        return [CARDS_FOLDER]


script_callbacks.on_before_ui(lambda: register_page(EasyTags()))
