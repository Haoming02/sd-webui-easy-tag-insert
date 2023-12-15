import modules.scripts as scripts
import shutil
import yaml
import time
import os
import re


SAMPLE_FOLDER = os.path.join(scripts.basedir(), 'samples')
TAGS_FOLDER = os.path.join(scripts.basedir(), 'tags')

TAGS = {}
ERRORS = []


def sanitize(item:str) -> str:
    return re.sub('[^a-zA-Z0-9 \.]', '', item).replace(' ', '_')

def sanitize_int(index:int) -> str:
    return f'{index:03}'


def check_dupe(A, parent:str):
    B = TAGS[parent]

    if isinstance(A, str):
        if A in B:
            ERRORS.append(f'Key Collision: "{parent}/{A}" Detected!')

    elif isinstance(A, dict):
        for k in A.keys():
            if k in B:
                ERRORS.append(f'Key Collision: "{parent}/{k}" Detected!')

    else:
        raise ValueError

def is_single_layer(item:dict) -> bool:
    for v in item.values():
        if not isinstance(v, str):
            return False

    return True

def parse_nested(parent:str, tags:dict):
    for k, v in tags.items():
        key = f'{parent}/{k}' if parent else k

        if isinstance(v, dict):
            if not is_single_layer(v):
                parse_nested(key, v)

            else:
                if key in TAGS:
                    check_dupe(v, key)
                    TAGS[key].update(v)
                else:
                    TAGS[key] = v

        else:
            if parent in TAGS:
                check_dupe(k, parent)
                TAGS[parent].update({k: v})
            else:
                TAGS[parent] = {k: v}

def load_dictionary(tags:dict):
    for key, value in tags.items():

        if isinstance(value, str):
            ERRORS.append(f'Top-Level Entry {{"{key}": "{value}"}} is not Supported...')
            continue

        if not is_single_layer(value):
            parse_nested(key, value)

        else:
            if key in TAGS:
                check_dupe(value, key)
                TAGS[key].update(value)
            else:
                TAGS[key] = value


# 1 sec
threshold = 1.0
last_executed = 0

def timegate() -> bool:
    global last_executed
    current_time = time.time()

    if (current_time - last_executed) >= threshold:
        last_executed = current_time
        return True

    return False


def reload_yaml():
    if not timegate():
        return []

    if not os.path.exists(TAGS_FOLDER):
        print('\n[Easy Tag Insert]: Folder "tags" not found. Initializing...\n')
        shutil.copytree(SAMPLE_FOLDER, TAGS_FOLDER)

    TAGS.clear()
    ERRORS.clear()

    for FILE in os.listdir(TAGS_FOLDER):
        if '.yml' not in FILE and '.yaml' not in FILE:
            print(f'Detected Non-YAML File: "{os.path.join(TAGS_FOLDER, FILE)}"...')
            continue

        with open(os.path.join(TAGS_FOLDER, FILE)) as stream:
            load_dictionary(yaml.safe_load(stream))

    return ERRORS
