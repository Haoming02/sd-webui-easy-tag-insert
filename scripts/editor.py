from modules import script_callbacks
from scripts.ez_utils import CARDS_FOLDER

import gradio as gr
import glob
import os


def clean_empty_folders(path: str):
    if not os.path.isdir(path):
        return

    if len(os.listdir(path)) > 0:
        for obj in os.listdir(path):
            clean_empty_folders(os.path.join(path, obj))

    if len(os.listdir(path)) == 0:
        os.remove(path)


def load():
    data: list[list] = []
    cards: list[str] = []

    objs = glob.glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)

    for obj in objs:
        if os.path.isdir(obj):
            continue

        if obj.endswith(".tag"):
            cards.append(obj)
        else:
            print(f'[EZ Tags] Invalid File: "{obj}"')

    for card in cards:
        path, ext = os.path.splitext(card)
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        category, name = relative_path.rsplit(os.sep, 1)

        with open(card, "r", encoding="utf-8") as card:
            prompt = card.read().strip()

        data.append([category, name, prompt])

    return data


def save(data: list):
    cards: list[str] = []
    objs = glob.glob(os.path.join(CARDS_FOLDER, "**", "*"), recursive=True)

    for obj in objs:
        if os.path.isdir(obj):
            continue
        if obj.endswith(".tag"):
            cards.append(obj)

    for category, name, prompt in data:
        category = category.strip()
        name = name.strip()
        prompt = prompt.strip()

        if (not category) or (not name) or (not prompt):
            continue

        folder = os.path.join(CARDS_FOLDER, category)
        if not os.path.exists(folder):
            os.makedirs(folder)

        card = os.path.join(folder, f"{name}.tag")

        if card in cards:
            cards.remove(card)

        with open(card, "w+", encoding="utf-8") as file:
            file.write(prompt)

    for card in cards:
        os.remove(card)

    for obj in os.listdir(CARDS_FOLDER):
        clean_empty_folders(os.path.join(CARDS_FOLDER, obj))


def editor_ui():

    with gr.Blocks() as TAGS_EDITOR:
        with gr.Row():
            save_btn = gr.Button("Save", variant="primary", interactive=False)
            load_btn = gr.Button("Load", interactive=True)

        tags = gr.Dataframe(
            label="Tags Editor",
            headers=["folder", "filename", "prompt"],
            datatype="str",
            row_count=(1, "dynamic"),
            col_count=(3, "fixed"),
            interactive=True,
            type="array",
        )

        load_btn.click(fn=load, inputs=None, outputs=[tags]).success(
            lambda: gr.update(interactive=True), inputs=None, outputs=[save_btn]
        )

        save_btn.click(fn=save, inputs=[tags], outputs=None)

    return [(TAGS_EDITOR, "EZ Tags Editor", "sd-webui-ez-tags-editor")]


script_callbacks.on_ui_tabs(editor_ui)
