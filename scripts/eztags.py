from modules import ui_extra_networks, shared, script_callbacks
from modules.ui_extra_networks import quote_js
import scripts.yaml_utils as yaml_utils
import modules.scripts as scripts
import shutil
import os


TEMP_FOLDER = os.path.join(scripts.basedir(), 'cards')


# ========== TEMP CARDS ==========
def setup_cards():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.makedirs(TEMP_FOLDER)

    for category, content in yaml_utils.TAGS.items():
        for key, value in content.items():

            FILENAME = f"{category.replace('/', '---')}___{key}.tag"
            with open(f'{os.path.join(TEMP_FOLDER, FILENAME)}', 'w') as F:
                F.write(value)
# ========== TEMP CARDS ==========


class EasyTags(ui_extra_networks.ExtraNetworksPage):

    def __init__(self):
        super().__init__('EZ Tags')
        self.allow_negative_prompt = True

    def refresh(self):
        logs = yaml_utils.reload_yaml()
        if logs:
            print('\n[Easy Tag Insert]:')
            print('\n'.join(logs) + "\n")

        setup_cards()

    def create_item(self, filename:str, i:str):
        with open(filename, 'r', encoding='utf-8') as F:
            prompt = F.read().strip()

        path, ext = os.path.splitext(filename)

        category = os.path.basename(path.split('___')[0]).replace('---', '/')
        name = path.split('___')[1]

        return {
            "name": name.strip(),
            "filename": filename,
            "shorthash": '.',
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_term": [category.strip(), name.strip()],
            "prompt": quote_js(prompt),
            "local_preview": f"{path}.preview.{shared.opts.samples_format}",
            "sort_keys": {
                'default': yaml_utils.sanitize(f'{category.lower()}-{name.lower()}'),
                "date_created": i,
                "date_modified": yaml_utils.sanitize(f'{category.lower()}-{i}'),
                'name': yaml_utils.sanitize(name.lower()),
            }
        }

    def list_items(self):
        i = 0
        for FILE in os.listdir(TEMP_FOLDER):
            i += 1
            yield self.create_item(os.path.join(TEMP_FOLDER, FILE), yaml_utils.sanitize_int(i))

    def allowed_directories_for_previews(self):
        return [TEMP_FOLDER]
# ========== LOADING STUFFS ==========


# ========== REGISTER CALLBACK ==========
def registerTab():
    if not os.path.exists(os.path.join(scripts.basedir(), 'tags')):
        yaml_utils.reload_yaml()
        setup_cards()

    ui_extra_networks.register_page(EasyTags())

script_callbacks.on_before_ui(registerTab)
# ========== REGISTER CALLBACK ==========
