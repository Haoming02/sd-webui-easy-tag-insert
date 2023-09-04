from pathlib import Path
import modules.scripts as scripts
import ruamel.yaml as yaml
import os

SAMP_FOLDER = Path(scripts.basedir()).joinpath('samples')
TAGS_FOLDER = Path(scripts.basedir()).joinpath('tags')

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
        os.rename(SAMP_FOLDER, TAGS_FOLDER)

    COLLECTION = {}

    for FILE in os.listdir(TAGS_FOLDER):
        if '.yml' not in FILE and '.yaml' not in FILE:
            print('Non-YAML File: "' + FILE + '" Found in Tags Folder')
            continue

        with open(TAGS_FOLDER.joinpath(FILE)) as stream:
            COLLECTION = merge_dictionary(COLLECTION, yaml.safe_load(stream))

    return COLLECTION
