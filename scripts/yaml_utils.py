from pathlib import Path
import modules.scripts as scripts
import ruamel.yaml as yaml
import os
import re

SAMPLE_FOLDER = Path(scripts.basedir()).joinpath('samples')
TAGS_FOLDER = Path(scripts.basedir()).joinpath('tags')

TAGS = {}

def sanitize(item:str):
    return re.sub('[^a-zA-Z0-9 \.]', '', item).replace(' ', '_')

def sanitize_int(index:int):
    return f'{index:03}'

def merge_dictionary(dict1, dict2):
    DICT = dict1.copy()
    for key, value in dict2.items():
        if key in DICT and isinstance(DICT[key], dict) and isinstance(value, dict):
            DICT[key] = merge_dictionary(DICT[key], value)
        else:
            DICT[key] = value
    return DICT

def reload_yaml():
    if not os.path.exists(TAGS_FOLDER):
        print('\n[Easy Tag Insert]: Folder "tags" not found. Initializing...\n')
        os.rename(SAMPLE_FOLDER, TAGS_FOLDER)

    global TAGS
    TAGS = {}

    for FILE in os.listdir(TAGS_FOLDER):
        if '.yml' not in FILE and '.yaml' not in FILE:
            print(f'Non-YAML File: "{FILE}" Found in Tags Folder')
            continue

        with open(TAGS_FOLDER.joinpath(FILE)) as stream:
            TAGS = merge_dictionary(TAGS, yaml.safe_load(stream))
