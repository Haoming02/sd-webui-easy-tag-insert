from modules.ui_extra_networks import ExtraNetworksPage, quote_js, register_page
from modules.script_callbacks import on_before_ui, on_ui_settings
from modules.shared import opts
from shutil import copytree
from glob import glob
import os


from lib_ez.settings import add_ui_settings, load_ui_settings
from lib_ez.utils import (
    EXAMPLE_FOLDER,
    CARDS_FOLDER,
    sanitize,
    sanitize_int,
)


class EasyTags(ExtraNetworksPage):

    def __init__(self):
        super().__init__("EZ Tags")
        self.allow_negative_prompt = True
        self.cards_db = None

        if not os.path.exists(CARDS_FOLDER):
            print('\n[EZ Tags] "cards" folder not found. Initializing...\n')
            copytree(EXAMPLE_FOLDER, CARDS_FOLDER)

        self.refresh()

    def refresh(self):
        self.cards_db: dict[str, str] = {}
        objs = glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)

        for path in objs:
            if not path.endswith(".tag"):
                continue

            name, _ = os.path.splitext(os.path.basename(path))
            if name in self.cards_db:
                print(f'\n[EZ Tags] Duplicated filename "{name}" was found!\n')

            self.cards_db.update({name: [path, None]})

    def create_item(self, name: str, index: str = None, *arg, **kwarg):
        if index is not None:
            self.cards_db[name][1] = index

        filename, index = self.cards_db[name]
        with open(filename, "r", encoding="utf-8") as card:
            prompt = card.readline().strip()

        path, ext = os.path.splitext(filename)
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        category, name = relative_path.rsplit(os.sep, 1)

        return {
            "name": name.strip(),
            "filename": filename,
            "shorthash": f"{hash(name)}",
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_terms": [self.search_terms_from_path(filename)],
            "prompt": quote_js(prompt),
            "local_preview": f"{path}.preview.{opts.samples_format}",
            "sort_keys": {
                "default": sanitize(f"{category}-{name}"),
                "date_created": index,
                "date_modified": sanitize(f"{category}-{index}"),
                "name": sanitize(name),
            },
        }

    def list_items(self):
        for i, name in enumerate(self.cards_db.keys()):
            yield self.create_item(name, sanitize_int(i + 1))

    def allowed_directories_for_previews(self):
        folders = set()
        objs = glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)
        for path in objs:
            if os.path.isdir(path):
                folders.add(path)

        return list(folders)


on_ui_settings(add_ui_settings)
on_before_ui(load_ui_settings)
on_before_ui(lambda: register_page(EasyTags()))
