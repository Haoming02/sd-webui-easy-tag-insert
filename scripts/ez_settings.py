from modules import script_callbacks, shared, scripts
import os


CSS = os.path.join(scripts.basedir(), "style.css")
section = ("ez", "EZ Tags")


def add_ui_settings():
    shared.opts.add_option(
        "ez_use_style",
        shared.OptionInfo(True, "Use custom style", section=section, category_id="ui")
        .info("Disable to use the built-in looks like LoRAs) (allow preview images")
        .needs_reload_ui(),
    )


def load_ui_settings():
    use_style = getattr(shared.opts, "ez_use_style", True)
    used_style = os.path.isfile(CSS)

    if used_style and os.path.isfile(f"{CSS}.bak"):
        os.remove(f"{CSS}.bak")

    if use_style and not used_style:
        os.rename(f"{CSS}.bak", CSS)
    if not use_style and used_style:
        os.rename(CSS, f"{CSS}.bak")


script_callbacks.on_ui_settings(add_ui_settings)
script_callbacks.on_before_ui(load_ui_settings)
