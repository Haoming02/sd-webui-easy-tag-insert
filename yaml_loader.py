from pathlib import Path
import modules.scripts as scripts
import ruamel.yaml as yaml
import os

TAGS_FOLDER = Path(scripts.basedir()).joinpath('tags')

def reload_yaml():
    COLLECTION = {}

    for FILE in os.listdir(TAGS_FOLDER):
        if '.yml' not in FILE and '.yaml' not in FILE:
            print('Non-YAML File: ' + FILE + ' Found in Tags Folder')
            continue

        with open(TAGS_FOLDER.joinpath(FILE)) as stream:
            COLLECTION.update(yaml.safe_load(stream))

    return COLLECTION