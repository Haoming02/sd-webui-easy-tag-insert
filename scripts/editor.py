from modules.script_callbacks import on_ui_tabs
from json import loads, dumps
from glob import glob
import gradio as gr
import os

from lib_ez import CARDS_FOLDER
from lib_ez.gradio import js

EZ_CACHE: dict[str, dict[str, str]] = {}


def delete_empty_folders(path: str):
    for par, folders, _ in os.walk(path, topdown=False):
        for folder in [os.path.join(par, f) for f in folders]:
            if not os.listdir(folder):
                os.rmdir(folder)


def load() -> str:
    EZ_CACHE.clear()
    cards: list[str] = glob(os.path.join(CARDS_FOLDER, "**", "*.tag"), recursive=True)

    if len(cards) == 0:
        gr.Warning(f'No valid ".tag" file found in "{CARDS_FOLDER}"...')
        return ""

    for card in cards:
        with open(card, "r", encoding="utf-8") as file:
            prompt = file.readline().strip()

        path, _ = os.path.splitext(card)
        relative_path = os.path.relpath(path, CARDS_FOLDER)
        category, name = relative_path.rsplit(os.sep, 1)

        if category not in EZ_CACHE:
            EZ_CACHE.update({category: {name: prompt}})
        else:
            EZ_CACHE[category].update({name: prompt})

    return dumps(EZ_CACHE)


def save(json_str: str):
    data: dict[str, dict[str, str]] = loads(json_str)
    changes: int = 0

    for category, cards in data.items():
        for name, prompt in cards.items():
            try:
                if EZ_CACHE[category][name] == prompt:
                    EZ_CACHE[category].pop(name)
                    continue
            except KeyError:
                pass

            os.makedirs(os.path.join(CARDS_FOLDER, category), exist_ok=True)
            with open(
                os.path.join(CARDS_FOLDER, category, f"{name}.tag"),
                encoding="utf-8",
                mode="w+",
            ) as card:
                card.write(f"{prompt}\n")
                changes += 1

    for category, cards in EZ_CACHE.items():
        for name, prompt in cards.items():
            if data.get(category, {}).get(name, False):
                continue

            os.remove(os.path.join(CARDS_FOLDER, category, f"{name}.tag"))
            changes += 1

    EZ_CACHE.clear()
    for k, v in data.items():
        EZ_CACHE.update({k: v})

    gr.Info(f"Cards Saved ({changes}x Change{'s' if changes > 1 else ''} Made)")
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
