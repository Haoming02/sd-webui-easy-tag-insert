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
        self.cards_db = None

        if os.path.exists(TAGS_FOLDER):
            print('\n[EZ Tags] "tags" folder has been deprecated. You may delete it~\n')
        if not os.path.exists(CARDS_FOLDER):
            print('\n[EZ Tags] "cards" folder not found. Initializing...\n')
            shutil.copytree(SAMPLE_FOLDER, CARDS_FOLDER)

        self.refresh()

    def refresh(self):
        self.cards_db: dict[str, str] = {}
        objs = glob.glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)

        for filename in objs:
            if os.path.isdir(filename):
                continue

            if not filename.endswith(".tag"):
                continue

            name = os.path.splitext(filename.rsplit(os.sep, 1)[1])[0]

            if name in self.cards_db:
                print(f'\n[EZ Tags] Duplicated filename "{name}" was found!\n')

            self.cards_db.update({name: [filename, -1]})

    def create_item(self, name: str, index: str = None, enable_filter: bool = True):
        if index is not None:
            self.cards_db[name][1] = index

        filename, index = self.cards_db[name]

        with open(filename, "r", encoding="utf-8") as card:
            prompt = card.read().strip()

        path, ext = os.path.splitext(filename)
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        category = relative_path.rsplit(os.sep, 1)[0]

        return {
            "name": name.strip(),
            "filename": filename,
            "shorthash": f"{hash(name)}",
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_terms": [self.search_terms_from_path(filename)],
            "prompt": quote_js(prompt),
            "local_preview": f"{path}.preview.{shared.opts.samples_format}",
            "sort_keys": {
                "default": sanitize(f"{category.lower()}-{name.lower()}"),
                "date_created": index,
                "date_modified": sanitize(f"{category.lower()}-{index}"),
                "name": sanitize(name.lower()),
            },
        }

    def list_items(self):
        i = 0

        for name in self.cards_db.keys():
            i += 1
            yield self.create_item(name, sanitize_int(i))

    def allowed_directories_for_previews(self):
        folders = set()
        folders.add(CARDS_FOLDER)

        objs = glob.glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)
        for obj in objs:
            if os.path.isdir(obj):
                folders.add(obj)

        return list(folders)


script_callbacks.on_before_ui(lambda: register_page(EasyTags()))
