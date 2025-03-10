from modules.ui_extra_networks import ExtraNetworksPage, quote_js, register_page
from modules.script_callbacks import on_before_ui, on_ui_settings
from modules.shared import opts
from glob import glob
import os.path

from lib_ez import EXAMPLE_FOLDER, CARDS_FOLDER
from lib_ez.utils import sanitize, sanitize_int
from lib_ez.settings import on_ez_settings


class EasyTags(ExtraNetworksPage):
    cards_db: dict[str, str] = {}

    def __init__(self):
        super().__init__("EZ-Tags")
        self.allow_negative_prompt = True

        if not os.path.exists(CARDS_FOLDER):
            from shutil import copytree

            print('\n[EZ Tags] "cards" folder not found. Initializing...\n')
            copytree(EXAMPLE_FOLDER, CARDS_FOLDER)

        self.refresh()

    def refresh(self):
        EasyTags.cards_db.clear()
        self.metadata.clear()

        objs = glob(os.path.join(CARDS_FOLDER, "**", "*.tag"), recursive=True)

        for path in objs:
            name, _ = os.path.splitext(os.path.basename(path))
            if name in EasyTags.cards_db:
                print(f'\n[EZ Tags] Duplicated filename "{name}" was found!\n')
                continue

            EasyTags.cards_db.update({name: path})

    def create_item(self, name: str, index: int = -1, *arg, **kwarg):
        filename = EasyTags.cards_db[name]
        with open(filename, "r", encoding="utf-8") as card:
            prompt = card.readline().strip()

        path = os.path.splitext(filename)[0]
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        name = os.path.basename(relative_path)
        category = relative_path[: -len(name)]

        return {
            "name": name.strip(),
            "filename": filename,
            "shorthash": f"{hash(name)}",
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_terms": [self.search_terms_from_path(filename)],
            "prompt": quote_js(prompt),
            "local_preview": f"{path}.preview.{opts.samples_format}",
            "metadata": prompt,
            "sort_keys": {
                "default": sanitize(f"{category}-{name}"),
                "date_created": index,
                "date_modified": sanitize(f"{category}-{index}"),
                "name": sanitize(name),
            },
        }

    def list_items(self):
        for i, name in enumerate(EasyTags.cards_db.keys()):
            yield self.create_item(name, sanitize_int(i + 1))

    def allowed_directories_for_previews(self):
        return [CARDS_FOLDER]


on_ui_settings(on_ez_settings)
on_before_ui(lambda: register_page(EasyTags()))
