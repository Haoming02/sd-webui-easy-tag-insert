import modules.scripts as scripts
import yaml
import shutil
import os
import re

SAMPLE_FOLDER = os.path.join(scripts.basedir(), 'samples')
TAGS_FOLDER = os.path.join(scripts.basedir(), 'tags')

TAGS = {}

def sanitize(item:str) -> str:
    return re.sub('[^a-zA-Z0-9 \.]', '', item).replace(' ', '_')

def sanitize_int(index:int) -> str:
    return f'{index:03}'

def is_single_layer(item:dict) -> bool:
    for v in item.values():
        if not isinstance(v, str):
            return False

    return True

def parse_nested(category:str, parent:str, tags:dict):
    global TAGS

    for k, v in tags.items():
        key = f'{parent}/{k}' if parent else k

        if isinstance(v, dict):
            parse_nested(category, key, v)

        else:
            if key in TAGS[category]:
                print(f'\n[Easy Tag Insert]: Duplicated Key [{category}/{key}] Detected!\n')

            TAGS[category].update({key: v})

def load_dictionary(tags:dict):
    global TAGS
    for key, value in tags.items():

        if isinstance(value, str):
            print(f'\n[Easy Tag Insert]: Top-Level Entry {{"{key}": "{value}"}} is not Supported...\n')
            continue

        if not is_single_layer(value):
            if key not in TAGS:
                TAGS[key] = {}

            parse_nested(key, '', value)

        else:
            if key not in TAGS:
                TAGS[key] = value
            else:
                for k in value.keys():
                    if k in TAGS[key]:
                        print(f'\n[Easy Tag Insert]: Duplicated Key [{key}/{k}] Detected!\n')

                TAGS[key].update(value)

def reload_yaml():
    if not os.path.exists(TAGS_FOLDER):
        print('\n[Easy Tag Insert]: Folder "tags" not found. Initializing...\n')
        shutil.copytree(SAMPLE_FOLDER, TAGS_FOLDER)

    global TAGS
    TAGS = {}

    for FILE in os.listdir(TAGS_FOLDER):
        if '.yml' not in FILE and '.yaml' not in FILE:
            print(f'Non-YAML File: "{FILE}" found in Tags folder...')
            continue

        with open(os.path.join(TAGS_FOLDER, FILE)) as stream:
            load_dictionary(yaml.safe_load(stream))
