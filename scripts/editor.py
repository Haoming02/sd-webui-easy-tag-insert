from modules.script_callbacks import on_ui_tabs
from json import loads, dumps
from glob import glob
import gradio as gr
import os

from lib_ez.utils import CARDS_FOLDER
from lib_ez.gradio import js

CACHE: dict = None
"""handle deletion"""


def delete_empty_folders(path: str):
    for par, folders, _ in os.walk(path, topdown=False):
        for folder in [os.path.join(par, f) for f in folders]:
            if not os.listdir(folder):
                os.rmdir(folder)


def load() -> str:
    global CACHE
    data: dict = {}
    cards: list[str] = [
        obj
        for obj in glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)
        if obj.endswith(".tag")
    ]

    if len(cards) == 0:
        gr.Warning('No Valid ".tag" File is Detected...')
        CACHE = {}
        return None

    for card in cards:
        with open(card, "r", encoding="utf-8") as file:
            prompt = file.readline().strip()

        path, ext = os.path.splitext(card)
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        category, name = relative_path.rsplit(os.sep, 1)

        if category not in data:
            data.update({category: {name: prompt}})
        else:
            data[category].update({name: prompt})

    CACHE = data
    return dumps(data)


def save(json_str: str):
    global CACHE
    data: dict = loads(json_str)
    changes: int = 0

    for category, cards in data.items():
        for name, prompt in cards.items():
            if (
                category in CACHE
                and name in CACHE[category]
                and prompt == CACHE[category][name]
            ):
                CACHE[category].pop(name)
                continue

            os.makedirs(os.path.join(CARDS_FOLDER, category), exist_ok=True)
            with open(
                os.path.join(CARDS_FOLDER, category, f"{name}.tag"),
                encoding="utf-8",
                mode="w+",
            ) as card:
                card.write(f"{prompt}\n")
                changes += 1

    for category, cards in CACHE.items():
        for name, prompt in cards.items():
            if data.get(category, {}).get(name, False):
                continue

            os.remove(os.path.join(CARDS_FOLDER, category, f"{name}.tag"))
            changes += 1

    CACHE = data
    gr.Info(f"Cards Saved ({changes}x Changes Made)")
    delete_empty_folders(CARDS_FOLDER)


def editor_ui():
    with gr.Blocks() as TAGS_EDITOR:
        with gr.Row():
            save_btn = gr.Button("Save", variant="primary", interactive=False)
            load_btn = gr.Button("Load")

        gr.HTML('<div id="ez-editor"></div>')

        with gr.Row(visible=False):
            tags = gr.Textbox(elem_id="ez-editor-box")
            real_save_btn = gr.Button("Save", elem_id="ez-editor-btn")

        save_btn.click(fn=None, **js("() => { EasyTagEditor.save(); }"))
        real_save_btn.click(fn=save, inputs=[tags])
        load_btn.click(fn=load, outputs=[tags]).success(
            fn=lambda: gr.update(interactive=True),
            outputs=[save_btn],
            **js("() => { EasyTagEditor.load(); }"),
        )

    return [(TAGS_EDITOR, "EZ Tags Editor", "sd-webui-ez-tags-editor")]


on_ui_tabs(editor_ui)
