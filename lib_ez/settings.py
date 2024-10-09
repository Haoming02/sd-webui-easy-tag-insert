from modules.shared import OptionInfo, opts
import os

from .utils import CSS


def add_ui_settings():
    opts.add_option(
        "ez_use_style",
        OptionInfo(
            True,
            "Use custom style",
            section=("ez", "EZ Tags"),
            category_id="ui",
        )
        .info("Disable to use the built-in ExtraNetwork looks) (allow preview images")
        .needs_reload_ui(),
    )


def load_ui_settings():
    use_style: bool = getattr(opts, "ez_use_style", True)
    used_style: bool = os.path.isfile(CSS)

    if used_style and os.path.isfile(f"{CSS}.bak"):
        os.remove(f"{CSS}.bak")

    if use_style and not used_style:
        os.rename(f"{CSS}.bak", CSS)
    if not use_style and used_style:
        os.rename(CSS, f"{CSS}.bak")
