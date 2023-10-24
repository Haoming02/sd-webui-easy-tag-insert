from modules import shared, ui_extra_networks, script_callbacks
from modules.ui_extra_networks import quote_js
import scripts.yaml_utils as yaml_utils
import html

class EasyTags(ui_extra_networks.ExtraNetworksPage):

# ========== LOADING STUFFS ==========
    def __init__(self):
        super().__init__('EZ Tags')

    def refresh(self):
        yaml_utils.reload_yaml()

    def create_item(self, category, index, name, i):
        return {
            "name": index,
            "prompt": name,
            "sort_keys": {
                'default': yaml_utils.sanitize(f'{category.lower()}-{index.lower()}'),
                "date_created": i,
                "date_modified": yaml_utils.sanitize(f'{category.lower()}-{i}'),
                'name': yaml_utils.sanitize(index.lower()),
            },
            "search_term": category,
        }

    def list_items(self):
        i = 0
        for category, content in yaml_utils.TAGS.items():
            for key, value in content.items():
                i += 1
                yield self.create_item(category, key, value, yaml_utils.sanitize_int(i))

    def allowed_directories_for_previews(self):
        return list(yaml_utils.TAGS.keys())
# ========== LOADING STUFFS ==========


# ========== HTML STUFFS ==========
    def create_html_for_item(self, item, tabname):
        """Create HTML for Card Item"""

        height = "height: 3em;"
        width = "width: 12em;"

        onclick = '"' + html.escape(f"""return cardClicked({quote_js(tabname)}, {quote_js(item["prompt"].strip())}, "true")""") + '"'

        sort_keys = " ".join([html.escape(f'data-sort-{k}={v}') for k, v in item.get("sort_keys", {}).items()]).strip()

        metadata_button = f"<div class='metadata-button card-button' title='Show Prompt' onclick='(function() {{ extraNetworksShowMetadata({quote_js(item['prompt'].strip())}); event.stopPropagation(); }}) ();'></div>"

        args = {
            "background_image": "",
            "style": f"'display: none; {height}{width}; background-image: linear-gradient(90deg, var(--button-secondary-background-fill), var(--button-primary-background-fill)); font-size: 100%'",
            "prompt": item.get("prompt", None),
            "tabname": quote_js(tabname),
            "local_preview": "",
            "name": html.escape(item["name"]),
            "description": "",
            "card_clicked": onclick,
            "save_card_preview": "",
            "search_term": item.get("search_term", ""),
            "metadata_button": metadata_button,
            "edit_button": "",
            "search_only": "",
            "sort_keys": sort_keys,
        }

        return self.card_page.format(**args)

    def create_html(self, tabname):
        items_html = ''

        subdirs = {}
        for cat in self.allowed_directories_for_previews():
            subdirs[cat] = 1

        if subdirs:
            subdirs = {"": 1, **subdirs}

        subdirs_html =  "".join([f"""
                        <button class='lg secondary gradio-button custom-button{" search-all" if subdir=="" else ""}' onclick='extraNetworksSearchButton("{tabname}_extra_search", event)'>
                        {html.escape(subdir if subdir!="" else "all")}
                        </button>""" for subdir in subdirs])

        self.items = {x["name"]: x for x in self.list_items()}

        for item in self.items.values():
            items_html += self.create_html_for_item(item, tabname)

        if items_html == '':
            dirs = "".join([f"<li>{x}</li>" for x in self.allowed_directories_for_previews()])
            items_html = shared.html("extra-networks-no-cards.html").format(dirs=dirs)

        self_name_id = self.name.replace(" ", "_")

        res =   f"""
                <div id='{tabname}_{self_name_id}_subdirs' class='extra-network-subdirs extra-network-subdirs-cards'>
                    {subdirs_html}
                </div>
                <div id='{tabname}_{self_name_id}_cards' class='extra-network-cards'>
                    {items_html}
                </div>
                """

        return res
# ========== HTML STUFFS ==========


# ========== REGISTER CALLBACK ==========
def registerTab():
    yaml_utils.reload_yaml()
    ui_extra_networks.register_page(EasyTags())

script_callbacks.on_before_ui(registerTab)
# ========== REGISTER CALLBACK ==========
